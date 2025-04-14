import streamlit as st
from helper import show_sidebar_guide

show_sidebar_guide()

st.title("Help & FAQs")

st.header("📖 How to Use the Dashboard")
st.markdown("""
1. **Upload Your Data**: Use the upload section to add your sales data in CSV or Excel format.
2. **Map Columns**: Ensure the columns for Order Date, Sales, and Profit are correctly mapped.
3. **Filter Data**: Use the filters to narrow down the data by date range or category.
4. **View Metrics**: Check the key metrics for a quick overview of your business performance.
5. **Forecast Revenue**: Use the forecasting section to predict future sales or profit.
6. **Analyze Profitability**: Identify the most and least profitable categories or products.
7. **Detect Anomalies**: Spot unusual spikes or drops in revenue.
8. **Download Data**: Export the filtered data for further analysis.
""")

st.header("❓ Frequently Asked Questions")
st.subheader("What file formats are supported?")
st.markdown("We support **CSV** and **Excel** files. Ensure your file is clean and formatted correctly.")

st.subheader("What columns are required?")
st.markdown("Your file should include at least the following columns: **Order Date**, **Sales**, and **Profit**.")

st.subheader("How is the forecast generated?")
st.markdown("We use the **Prophet** library to generate forecasts based on historical data.")

st.subheader("Can I change the currency?")
st.markdown("Yes, use the currency selector to convert values to your preferred currency.")

st.subheader("What happens if I refresh the page?")
st.markdown("Your progress is saved using session state, so you won't lose your data or settings.")