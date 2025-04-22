import streamlit as st
from helper import show_sidebar_guide

if 'selected_currency' not in st.session_state:
    st.session_state.selected_currency = "USD"

st.title("💰 Profitability Insights")
st.markdown("💰 This page shows which categories or products are the most (or least) profitable based on their **Profit Margin**.")

show_sidebar_guide()

# Read data from session state
data = st.session_state.get('cleaned_data', None)
if data is None:
    st.error("No data available. Please upload a file on the Upload page.")
    st.stop()

# Global column map helper
profit_column = st.session_state.column_map.get('Profit')
sales_column = st.session_state.column_map.get('Sales')
product_column = st.session_state.column_map.get('Product')

# Check for required columns and provide warnings
if not profit_column or profit_column not in data.columns:
    st.warning("Profit column is missing or not mapped. Profitability insights may not be available.")
if not sales_column or sales_column not in data.columns:
    st.warning("Sales column is missing or not mapped. Profitability insights may not be available.")

# Profitability insights
view_option = st.radio("View Profitability Insights for:", ["Categories", "Products"])

# Graceful feature skipping
try:
    if view_option == "Categories" and 'Category' in data.columns:
        profitability = data.groupby('Category').agg({'Profit': 'sum', 'Sales': 'sum'}).reset_index()
        profitability['Profit Margin (%)'] = (profitability['Profit'] / profitability['Sales']) * 100
        most_profitable = profitability.sort_values(by='Profit Margin (%)', ascending=False).head(3)
        least_profitable = profitability.sort_values(by='Profit Margin (%)').head(3)

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Top 3 Most Profitable Categories")
            st.dataframe(most_profitable)
        with col2:
            st.subheader("Top 3 Least Profitable Categories")
            st.dataframe(least_profitable)
    elif view_option == "Products" and product_column and product_column in data.columns:
        profitability = data.groupby(product_column).agg({"Profit": "sum", "Sales": "sum"}).reset_index()
        profitability['Profit Margin (%)'] = (profitability['Profit'] / profitability['Sales']) * 100
        most_profitable = profitability.sort_values(by='Profit Margin (%)', ascending=False).head(3)
        least_profitable = profitability.sort_values(by='Profit Margin (%)').head(3)

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Top 3 Most Profitable Products")
            st.dataframe(most_profitable)
        with col2:
            st.subheader("Top 3 Least Profitable Products")
            st.dataframe(least_profitable)
    else:
        st.warning("The selected option is not available or required columns are not mapped correctly.")
except KeyError as e:
    st.info(f"Profitability insights couldn't be generated because a required column is missing: {e}")

# Feature requirements badges
st.markdown("### 💰 Profitability Insights _(requires: Profit, Sales)_")