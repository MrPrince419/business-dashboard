import streamlit as st
import pandas as pd
import numpy as np
from prophet import Prophet
import plotly.graph_objects as go
from datetime import datetime
from fpdf import FPDF
import tempfile
import os

# Page setup
st.set_page_config(page_title="Business Dashboard", layout="wide", page_icon="📈")
st.markdown("# Business Dashboard")

# Upload Section
st.markdown("## Upload Your Business Data")
file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

@st.cache_data
def load_data(file):
    try:
        if file.name.endswith(".csv"):
            return pd.read_csv(file, encoding_errors='ignore')
        elif file.name.endswith(".xlsx"):
            return pd.read_excel(file)
    except Exception as e:
        st.error(f"Failed to load file: {e}")
        return None

@st.cache_data
def compute_forecast(data, months):
    m = Prophet()
    m.fit(data)
    future = m.make_future_dataframe(periods=months * 30)
    return m.predict(future)

data = None
if file:
    data = load_data(file)
    if data is not None:
        st.success("File uploaded and processed successfully!")
        st.dataframe(data.head())
    else:
        st.stop()
else:
    st.stop()

# Preprocessing
required_columns = ['Order Date', 'Sales', 'Profit']
missing_columns = [col for col in required_columns if col not in data.columns]
if missing_columns:
    st.error(f"The uploaded file is missing the following required columns: {', '.join(missing_columns)}")
    st.stop()

st.markdown("### Map Your Columns")

# Try to find defaults
def find_default(col_options, keywords):
    for kw in keywords:
        for col in col_options:
            if kw.lower() in col.lower():
                return col
    return col_options[0]  # fallback

order_date_default = find_default(data.columns, ["order date", "date"])
sales_default = find_default(data.columns, ["sales", "revenue"])
profit_default = find_default(data.columns, ["profit", "margin"])

order_date_col = st.selectbox("Select the 'Order Date' column", data.columns, index=data.columns.get_loc(order_date_default))
sales_col = st.selectbox("Select the 'Sales' column", data.columns, index=data.columns.get_loc(sales_default))
profit_col = st.selectbox("Select the 'Profit' column", data.columns, index=data.columns.get_loc(profit_default))

try:
    data['Order Date'] = pd.to_datetime(data[order_date_col])
    data['Sales'] = pd.to_numeric(data[sales_col], errors='coerce')
    data['Profit'] = pd.to_numeric(data[profit_col], errors='coerce')
except Exception as e:
    st.error("Could not parse necessary columns. Ensure your file contains 'Order Date', 'Sales', and 'Profit'.")
    st.stop()

# Filter by date range
st.markdown("## Filter by Date Range")
min_date, max_date = data['Order Date'].min(), data['Order Date'].max()
date_range = st.date_input("Select Date Range", value=(min_date, max_date), min_value=min_date, max_value=max_date)
data = data[(data['Order Date'] >= pd.to_datetime(date_range[0])) & (data['Order Date'] <= pd.to_datetime(date_range[1]))]

st.markdown("### Filter by Category")
if 'Category' in data.columns:
    category_filter = st.multiselect("Select Categories", options=data['Category'].unique(), default=data['Category'].unique())
    data = data[data['Category'].isin(category_filter)]

# Metrics
st.markdown("## Key Metrics")
kpi1, kpi2 = st.columns(2)
kpi3, kpi4 = st.columns(2)
with kpi1:
    st.metric("Total Orders", len(data))
with kpi2:
    st.metric("Total Revenue", f"${data['Sales'].sum():,.2f}")
with kpi3:
    st.metric("Avg Order Value", f"${data['Sales'].mean():,.2f}")
with kpi4:
    st.metric("Total Profit", f"${data['Profit'].sum():,.2f}")

# Forecasting
st.markdown("## Forecasting: Revenue Prediction")
months = st.slider("Select number of months to forecast:", 1, 12, 3)
forecast_metric = st.selectbox("Select Metric to Forecast", ['Sales', 'Profit'])
df_daily = data.groupby('Order Date').agg({forecast_metric: 'sum'}).reset_index()
df_daily.columns = ['ds', 'y']

# Ensure there are at least 2 non-NaN rows for forecasting
if df_daily['y'].dropna().shape[0] < 2:
    st.error("Not enough clean data to forecast this metric. Please upload more data or adjust your filters.")
    st.stop()

forecast = compute_forecast(df_daily, months)

st.markdown("### Forecast Chart")
fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], mode='lines', name='Forecast'))
fig1.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat_upper'], mode='lines', name='Upper Bound', line=dict(dash='dot')))
fig1.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat_lower'], mode='lines', name='Lower Bound', line=dict(dash='dot')))
fig1.update_layout(title='Revenue Forecast (with Confidence Interval)', xaxis_title='Date', yaxis_title='Revenue')
st.plotly_chart(fig1)

st.markdown("### Forecast Summary (Month by Month)")
forecast['Month'] = forecast['ds'].dt.to_period('M').dt.to_timestamp()
monthly_forecast = forecast.groupby('Month')['yhat'].sum().reset_index()

fig2 = go.Figure()
fig2.add_trace(go.Bar(
    x=monthly_forecast['Month'],
    y=monthly_forecast['yhat'],
    name='Forecasted Revenue',
    marker_color='blue'
))
fig2.update_layout(
    title='Forecast Summary (Month by Month)',
    xaxis_title='Month',
    yaxis_title='Forecasted Revenue',
    showlegend=True
)
st.plotly_chart(fig2)

# Forecast Accuracy
st.markdown("## Forecast Accuracy")
if 'Actual' in forecast.columns:  # Assuming 'Actual' column exists in forecast
    forecast['Error'] = forecast['Actual'] - forecast['yhat']
    forecast['Accuracy (%)'] = (1 - abs(forecast['Error'] / forecast['Actual'])) * 100
    avg_accuracy = forecast['Accuracy (%)'].mean()
    st.metric("Average Forecast Accuracy", f"{avg_accuracy:.2f}%")

# Anomaly Detection
st.markdown("## Revenue Anomalies")
data['Month'] = data['Order Date'].dt.to_period("M")
monthly_revenue = data.groupby('Month')['Sales'].sum().reset_index()
monthly_revenue['Month'] = monthly_revenue['Month'].dt.to_timestamp()
mean = monthly_revenue['Sales'].mean()
deviation = monthly_revenue['Sales'].std()

sensitivity = st.slider("Anomaly Detection Sensitivity (% from average)", 10, 100, 30)
thresh = (sensitivity / 100) * mean
monthly_revenue['Type'] = monthly_revenue['Sales'].apply(lambda x: 'Spike' if x > mean + thresh else ('Drop' if x < mean - thresh else 'Normal'))

fig2 = go.Figure()
fig2.add_trace(go.Scatter(
    x=monthly_revenue['Month'],
    y=monthly_revenue['Sales'],
    mode='lines+markers',
    name='Monthly Revenue',
    line=dict(color='gray')
))
fig2.add_trace(go.Scatter(
    x=monthly_revenue[monthly_revenue['Type'] == 'Spike']['Month'],
    y=monthly_revenue[monthly_revenue['Type'] == 'Spike']['Sales'],
    mode='markers',
    name='Spike',
    marker=dict(color='red', size=10)
))
fig2.add_trace(go.Scatter(
    x=monthly_revenue[monthly_revenue['Type'] == 'Drop']['Month'],
    y=monthly_revenue[monthly_revenue['Type'] == 'Drop']['Sales'],
    mode='markers',
    name='Drop',
    marker=dict(color='blue', size=10)
))
fig2.update_layout(
    title='Monthly Revenue with Spikes and Drops',
    xaxis_title='Month',
    yaxis_title='Revenue',
    showlegend=True
)
st.plotly_chart(fig2)

# Export Section
st.markdown("## Share or Download")
b1, b2 = st.columns(2)
with b1:
    csv = data.to_csv(index=False).encode('utf-8')
    st.download_button("Download Data as CSV", csv, "filtered_data.csv", "text/csv")

def export_to_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Business Dashboard Report", ln=True, align='C')
    pdf.cell(200, 10, txt=f"Total Revenue: ${data['Sales'].sum():,.2f}".encode("latin1", errors="replace").decode("latin1"), ln=True)
    pdf.cell(200, 10, txt=f"Total Profit: ${data['Profit'].sum():,.2f}".encode("latin1", errors="replace").decode("latin1"), ln=True)
    date_line = f"Date Range: {data['Order Date'].min().date()} -> {data['Order Date'].max().date()}"
    pdf.cell(200, 10, txt=date_line.encode("latin1", errors="replace").decode("latin1"), ln=True)
    
    pdf.cell(200, 10, txt="Anomalies Summary:", ln=True)
    for _, row in monthly_revenue.iterrows():
        anomaly_line = f"{row['Month'].date()}: {row['Type']} (${row['Sales']:,.2f})"
        pdf.cell(200, 10, txt=anomaly_line.encode("latin1", errors="replace").decode("latin1"), ln=True)
    
    pdf.cell(200, 10, txt="Forecast Summary:", ln=True)
    for _, row in forecast[['ds', 'yhat']].tail(5).iterrows():
        forecast_line = f"{row['ds'].date()}: ${row['yhat']:,.2f}"
        pdf.cell(200, 10, txt=forecast_line.encode("latin1", errors="replace").decode("latin1"), ln=True)
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
        pdf.output(tmpfile.name)
        return tmpfile.name

with b2:
    if st.button("Export Report as PDF"):
        pdf_path = export_to_pdf()
        with open(pdf_path, "rb") as pdf_file:
            st.download_button("Download PDF Report", pdf_file, "dashboard_report.pdf", "application/pdf")

