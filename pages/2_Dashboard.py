import streamlit as st
from helper import show_sidebar_guide

st.title("📊 Dashboard")
st.markdown("This page provides key metrics to give you an overview of your business performance based on the filtered data.")

# Initialize selected_currency in session state
if 'selected_currency' not in st.session_state:
    st.session_state.selected_currency = "USD"

# Read data from session state
data = st.session_state.get('cleaned_data', None)
if data is None:
    st.error("No data available. Please upload a file on the Upload page.")
    st.stop()

# Display metrics
kpi1, kpi2 = st.columns(2)
kpi3, kpi4 = st.columns(2)
with kpi1:
    st.metric("Total Orders", len(data))
with kpi2:
    st.metric("Total Revenue", f"{data['Sales'].sum():,.2f} {st.session_state.selected_currency}")
with kpi3:
    st.metric("Avg Order Value", f"{data['Sales'].mean():,.2f} {st.session_state.selected_currency}")
with kpi4:
    st.metric("Total Profit", f"{data['Profit'].sum():,.2f} {st.session_state.selected_currency}")

show_sidebar_guide()