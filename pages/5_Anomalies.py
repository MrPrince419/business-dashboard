import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from helper import show_sidebar_guide, handle_missing_columns

st.title("⚠️ Revenue Anomalies")
st.markdown("This page helps you identify months where revenue was unusually high (**spike**) or low (**drop**) compared to the average.")

# Read data from session state
data = st.session_state.get('cleaned_data', None)
if data is None:
    st.error("No data available. Please upload a file on the Upload page.")
    st.stop()

if 'selected_currency' not in st.session_state:
    st.session_state.selected_currency = "USD"

# Global column map helper
order_date_column = st.session_state.column_map.get('Order Date')
sales_column = st.session_state.column_map.get('Sales')

# Check for required columns and provide warnings
if not order_date_column or order_date_column not in data.columns:
    st.warning("Order Date column is missing or not mapped. Anomaly detection may not be available.")
if not sales_column or sales_column not in data.columns:
    st.warning("Sales column is missing or not mapped. Anomaly detection may not be available.")

# Graceful feature skipping
try:
    data[order_date_column] = pd.to_datetime(data[order_date_column], errors='coerce')

    # Anomaly detection settings
    with st.expander("Anomaly Detection Settings"):
        sensitivity = st.slider("Anomaly Detection Sensitivity (% from average)", 10, 100, 30)

    # Perform anomaly detection
    data['Month'] = data[order_date_column].dt.to_period("M")
    monthly_revenue = data.groupby('Month')[sales_column].sum().reset_index()
    monthly_revenue['Month'] = monthly_revenue['Month'].dt.to_timestamp()
    mean = monthly_revenue[sales_column].mean()
    thresh = (sensitivity / 100) * mean
    monthly_revenue['Type'] = monthly_revenue[sales_column].apply(lambda x: 'Spike' if x > mean + thresh else ('Drop' if x < mean - thresh else 'Normal'))

    # Display anomaly chart
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=monthly_revenue['Month'],
        y=monthly_revenue[sales_column],
        mode='lines+markers',
        name='Monthly Revenue',
        line=dict(color='gray')
    ))
    fig3.add_trace(go.Scatter(
        x=monthly_revenue[monthly_revenue['Type'] == 'Spike']['Month'],
        y=monthly_revenue[monthly_revenue['Type'] == 'Spike'][sales_column],
        mode='markers',
        name='Spike',
        marker=dict(color='red', size=10)
    ))
    fig3.add_trace(go.Scatter(
        x=monthly_revenue[monthly_revenue['Type'] == 'Drop']['Month'],
        y=monthly_revenue[monthly_revenue['Type'] == 'Drop'][sales_column],
        mode='markers',
        name='Drop',
        marker=dict(color='blue', size=10)
    ))
    fig3.update_layout(
        title='Monthly Revenue with Spikes and Drops',
        xaxis_title='Month',
        yaxis_title=f"Sales ({st.session_state.selected_currency})",
        showlegend=True
    )
    st.plotly_chart(fig3)
except KeyError as e:
    st.info(f"Anomaly detection couldn't be generated because a required column is missing: {e}")

# Feature requirements badges
st.markdown("### ⚠️ Revenue Anomalies _(requires: Order Date, Sales)_")

show_sidebar_guide()