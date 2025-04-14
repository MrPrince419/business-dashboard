import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from helper import show_sidebar_guide

st.title("⚠️ Revenue Anomalies")
st.markdown("This page helps you identify months where revenue was unusually high (**spike**) or low (**drop**) compared to the average.")

# Read data from session state
data = st.session_state.get('cleaned_data', None)
if data is None:
    st.error("No data available. Please upload a file on the Upload page.")
    st.stop()

if 'selected_currency' not in st.session_state:
    st.session_state.selected_currency = "USD"

data['Order Date'] = pd.to_datetime(data['Order Date'], errors='coerce')

# Anomaly detection settings
with st.expander("Anomaly Detection Settings"):
    sensitivity = st.slider("Anomaly Detection Sensitivity (% from average)", 10, 100, 30)

# Perform anomaly detection
data['Month'] = data['Order Date'].dt.to_period("M")
monthly_revenue = data.groupby('Month')['Sales'].sum().reset_index()
monthly_revenue['Month'] = monthly_revenue['Month'].dt.to_timestamp()
mean = monthly_revenue['Sales'].mean()
thresh = (sensitivity / 100) * mean
monthly_revenue['Type'] = monthly_revenue['Sales'].apply(lambda x: 'Spike' if x > mean + thresh else ('Drop' if x < mean - thresh else 'Normal'))

# Display anomaly chart
fig3 = go.Figure()
fig3.add_trace(go.Scatter(
    x=monthly_revenue['Month'],
    y=monthly_revenue['Sales'],
    mode='lines+markers',
    name='Monthly Revenue',
    line=dict(color='gray')
))
fig3.add_trace(go.Scatter(
    x=monthly_revenue[monthly_revenue['Type'] == 'Spike']['Month'],
    y=monthly_revenue[monthly_revenue['Type'] == 'Spike']['Sales'],
    mode='markers',
    name='Spike',
    marker=dict(color='red', size=10)
))
fig3.add_trace(go.Scatter(
    x=monthly_revenue[monthly_revenue['Type'] == 'Drop']['Month'],
    y=monthly_revenue[monthly_revenue['Type'] == 'Drop']['Sales'],
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

show_sidebar_guide()