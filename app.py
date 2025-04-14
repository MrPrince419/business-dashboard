import streamlit as st
import pandas as pd
from prophet import Prophet
import plotly.graph_objects as go
from helper import download_data, describe, drop_items, rename_columns, handling_missing_values, clear_image_cache, fetch_exchange_rate
import os
import pickle

# Page setup
st.set_page_config(page_title="Business Dashboard", layout="wide", page_icon="📈")

st.title("📈 Business Dashboard")
st.markdown("Welcome to your smart business analytics dashboard.")

st.header("📖 What is this dashboard?")
st.markdown("""
This is an interactive tool designed to help you:
- Understand your business performance at a glance
- Forecast future sales and profits
- Identify trends, spikes, or dips in revenue
- Analyze profitability by product or category
- Download filtered reports for sharing or records
""")

st.header("🛠️ How to Use It (Step-by-Step)")
st.markdown("""
1. **Upload**: Add your data file (CSV/Excel) in the **Upload** tab.
2. **Dashboard**: See key metrics like total revenue, profit, and average order value.
3. **Forecasting**: Predict future Sales or Profit using your historical data.
4. **Profitability**: Find out your top and worst performing categories/products.
5. **Anomalies**: Spot revenue spikes or unusual drops.
6. **Export**: Download your filtered data as a CSV.
7. **Help**: Check FAQs and guides.

> Use the left sidebar to navigate between pages.
""")

st.header("💡 Pro Tip")
st.info("You don’t need to restart — all your uploaded and filtered data will stay as long as the session is active.")

