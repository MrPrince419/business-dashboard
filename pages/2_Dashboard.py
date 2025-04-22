import streamlit as st
from helper import show_sidebar_guide, fetch_exchange_rate, handle_missing_columns, generate_summary
import pandas as pd
from datetime import datetime
import numpy as np

st.title("📊 Dashboard")
st.markdown("This page provides key metrics to give you an overview of your business performance based on the filtered data.")

# Initialize selected_currency in session state
if 'selected_currency' not in st.session_state:
    st.session_state.selected_currency = "USD"

# Add currency selection dropdown with top 5 currencies and Naira
currency_options = ["USD", "EUR", "GBP", "JPY", "AUD", "NGN"]
selected_currency = st.sidebar.selectbox("Select Currency", currency_options, index=currency_options.index(st.session_state.selected_currency))

# Fetch exchange rate and update session state
if selected_currency != st.session_state.selected_currency:
    exchange_rate = fetch_exchange_rate(base_currency="USD", target_currency=selected_currency)
    st.session_state.selected_currency = selected_currency
    st.session_state.exchange_rate = exchange_rate

# Apply currency conversion to metrics
exchange_rate = st.session_state.get('exchange_rate', 1.0)

# Read data from session state
data = st.session_state.get('cleaned_data', None)
if data is None:
    st.error("No data available. Please upload a file on the Upload page.")
    st.stop()

# Global column map helper
sales_column = st.session_state.column_map.get('Sales')
profit_column = st.session_state.column_map.get('Profit')
order_date_column = st.session_state.column_map.get('Order Date')
product_column = st.session_state.column_map.get('Product', 'Product')  # Default to 'Product' if not mapped

# Check for required columns and provide warnings
if not sales_column or sales_column not in data.columns:
    st.warning("Sales column is missing or not mapped. Some metrics may not be available.")
if not profit_column or profit_column not in data.columns:
    st.warning("Profit column is missing or not mapped. Some metrics may not be available.")
if not order_date_column or order_date_column not in data.columns:
    st.warning("Order Date column is missing or not mapped. Some metrics may not be available.")
if product_column not in data.columns:
    st.warning("Product column is missing or not mapped. Product-specific insights will not be available.")

# Add date filter if 'Order Date' column is valid
if order_date_column and order_date_column in data.columns:
    min_date = pd.to_datetime(data[order_date_column], errors='coerce').min()
    max_date = pd.to_datetime(data[order_date_column], errors='coerce').max()

    start_date, end_date = st.date_input("📅 Select Date Range", [min_date, max_date])
    data[order_date_column] = pd.to_datetime(data[order_date_column], errors="coerce")
    data = data[(data[order_date_column] >= pd.to_datetime(start_date)) & (data[order_date_column] <= pd.to_datetime(end_date))]

# Optional filters for KPIs
with st.expander("📍 Filter Metrics (Optional)"):
    category_filter = st.multiselect("Filter by Category", options=data.get("Category", pd.Series()).dropna().unique())
    region_filter = st.multiselect("Filter by Region", options=data.get("Region", pd.Series()).dropna().unique())
    segment_filter = st.multiselect("Filter by Segment", options=data.get("Segment", pd.Series()).dropna().unique())

    if category_filter:
        data = data[data["Category"].isin(category_filter)]
    if region_filter:
        data = data[data["Region"].isin(region_filter)]
    if segment_filter:
        data = data[data["Segment"].isin(segment_filter)]

# Graceful feature skipping
try:
    with st.spinner("Calculating metrics..."):
        kpi1, kpi2 = st.columns(2)
        kpi3, kpi4 = st.columns(2)
        with kpi1:
            st.metric("Total Orders", len(data))
            with st.expander("🧠 What does this mean?"):
                st.markdown("**Total Orders** is the total number of individual purchases made by your customers during the selected time period.")
        with kpi2:
            st.metric("Total Revenue", f"{(data[sales_column].sum() * exchange_rate):,.2f} {st.session_state.selected_currency}")
            with st.expander("🧠 What does this mean?"):
                st.markdown("**Total Revenue** is the total amount of money your business earned from sales during the selected time. It’s not your profit — just the total income from selling products or services.")
        with kpi3:
            st.metric("Avg Order Value", f"{(data[sales_column].mean() * exchange_rate):,.2f} {st.session_state.selected_currency}")
            with st.expander("🧠 What does this mean?"):
                st.markdown("**Avg Order Value** is the average amount of money spent by a customer per order. It’s calculated by dividing Total Revenue by Total Orders.")
        with kpi4:
            st.metric("Total Profit", f"{(data[profit_column].sum() * exchange_rate):,.2f} {st.session_state.selected_currency}")
            with st.expander("🧠 What does this mean?"):
                st.markdown("**Total Profit** is the amount of money your business made after subtracting all costs from Total Revenue. It’s a key indicator of your business’s financial health.")
except KeyError as e:
    st.info(f"Some metrics couldn't be generated because a required column is missing: {e}")

# Feature requirements badges
st.markdown("### 📊 Total Revenue _(requires: Sales)_")
st.markdown("### 📈 Total Profit _(requires: Profit)_")
st.markdown("### 📅 Order Insights _(requires: Order Date)_")

# Ensure 'Order Date' is converted to datetime
if order_date_column and order_date_column in data.columns:
    data[order_date_column] = pd.to_datetime(data[order_date_column], errors='coerce')
    # Handle cases where conversion fails
    data = data.dropna(subset=[order_date_column])

    # Add quick insights
    st.subheader("Quick Insights")
    
    # Rename 'Order Date' to standard name for processing
    data['Order Date'] = data[order_date_column]
    
    current_month = data['Order Date'].dt.to_period('M').max()
    last_month = current_month - 1

    # Top product this month - Only show if Product column exists
    if product_column in data.columns:
        try:
            top_product = data[data['Order Date'].dt.to_period('M') == current_month].groupby(product_column)[sales_column].sum().idxmax()
            st.metric("Top Product This Month", top_product)
        except (KeyError, ValueError) as e:
            st.warning(f"Unable to identify top product: {e}")
    else:
        st.info("Product insights not available - 'Product' column is missing or not mapped.")

    # Worst-performing category last quarter - Only show if Category column exists
    if 'Category' in data.columns:
        try:
            last_quarter = current_month - 3
            data_last_quarter = data[data['Order Date'].dt.to_period('Q') == last_quarter]
            grouped = data_last_quarter.groupby('Category')[profit_column].sum()
            if not grouped.empty:
                worst_category = grouped.idxmin()
                st.metric("Worst Category (Last Quarter)", worst_category)
            else:
                st.warning("No data available for the selected quarter.")
        except (KeyError, ValueError) as e:
            st.warning(f"Unable to identify worst category: {e}")

    # Sales comparison to last month
    try:
        sales_current = data[data['Order Date'].dt.to_period('M') == current_month][sales_column].sum()
        sales_last = data[data['Order Date'].dt.to_period('M') == last_month][sales_column].sum()
        sales_change = ((sales_current - sales_last) / sales_last) * 100 if sales_last != 0 else 0
        st.metric("Sales Change from Last Month", f"{sales_change:.2f}%")
    except (KeyError, ValueError) as e:
        st.warning(f"Unable to calculate sales change: {e}")

    # Executive Summary
    with st.expander("📄 Executive Summary Report"):
        st.markdown("Here’s a high-level overview of your business performance for the current period.")

        try:
            summary_lines = [
                f"🗓 **Period**: {current_month.strftime('%B %Y')}",
                f"💰 **Revenue**: ${sales_current:,.2f}"
            ]
            
            # Add profit if available
            if profit_column in data.columns:
                summary_lines.append(f"📈 **Profit**: ${data[data['Order Date'].dt.to_period('M') == current_month][profit_column].sum():,.2f}")
            
            # Add top product if available
            if product_column in data.columns and 'top_product' in locals():
                summary_lines.append(f"🥇 **Top Product**: {top_product}")
            
            # Add worst category if available
            if 'Category' in data.columns and 'worst_category' in locals():
                summary_lines.append(f"📉 **Worst Category Last Quarter**: {worst_category}")
            
            # Add sales change
            if 'sales_change' in locals():
                summary_lines.append(f"📊 **Sales Change from Last Month**: {sales_change:.2f}%")

            for line in summary_lines:
                st.markdown(line)

            st.info("✅ This will be included in the future PDF export feature.")
        except Exception as e:
            st.warning(f"Unable to generate complete summary: {e}")

def generate_smart_summary(data, date_col, sales_col, profit_col):
    if data is None or date_col not in data.columns or sales_col not in data.columns:
        return "Not enough data for insights."

    df = data.copy()
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
    df.dropna(subset=[date_col], inplace=True)
    df['Month'] = df[date_col].dt.to_period("M")

    try:
        recent_month = df['Month'].max()
        prev_month = recent_month - 1
        recent_data = df[df['Month'] == recent_month]
        prev_data = df[df['Month'] == prev_month]

        sales_change = recent_data[sales_col].sum() - prev_data[sales_col].sum()
        
        # Only calculate profit change if profit column exists
        profit_text = ""
        if profit_col in df.columns:
            profit_change = recent_data[profit_col].sum() - prev_data[profit_col].sum()
            profit_text = f"- Profit change this month: ${profit_change:,.2f}  \n"
            
        # Only calculate top product if Product column exists
        product_text = ""
        product_column = st.session_state.column_map.get('Product', 'Product')
        if product_column in df.columns:
            try:
                top_product = recent_data.groupby(product_column)[profit_col if profit_col in df.columns else sales_col].sum().idxmax()
                product_text = f"- 🥇 Most profitable product: **{top_product}**  \n"
            except Exception:
                product_text = ""

        insight = f"""
        📊 **Smart Summary**  
        - Sales change this month: ${sales_change:,.2f}  
        {profit_text}{product_text}
        """
        return insight
    except Exception as e:
        return "Unable to generate summary: " + str(e)

# Add Smart Summary section
if st.session_state.get("cleaned_data") is not None:
    df = st.session_state.cleaned_data
    sales_col = st.session_state.column_map.get("Sales")
    profit_col = st.session_state.column_map.get("Profit")
    date_col = st.session_state.column_map.get("Order Date")

    st.markdown(generate_smart_summary(df, date_col, sales_col, profit_col))

# Add Smart Insights section
if data is not None:
    st.markdown("### 🧠 Smart Insights (Auto-Generated)")
    summary = generate_summary(data, st.session_state.column_map)
    st.info(summary)

def generate_insight_cards(data, date_col, sales_col, profit_col):
    if data is None or date_col not in data.columns or sales_col not in data.columns:
        return ["Not enough data for insights."]

    df = data.copy()
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
    df.dropna(subset=[date_col], inplace=True)
    df['Month'] = df[date_col].dt.to_period("M")

    insights = []

    try:
        recent_month = df['Month'].max()
        prev_month = recent_month - 1
        recent_data = df[df['Month'] == recent_month]
        prev_data = df[df['Month'] == prev_month]

        # Revenue change
        sales_change = recent_data[sales_col].sum() - prev_data[sales_col].sum()
        sales_change_pct = (sales_change / prev_data[sales_col].sum() * 100) if prev_data[sales_col].sum() != 0 else 0
        if sales_change_pct > 0:
            insights.append(f"💰 This month's revenue is up by {sales_change_pct:.2f}% compared to last month.")
        else:
            insights.append(f"📉 Revenue dropped by {abs(sales_change_pct):.2f}% compared to last month.")

        # Profit change - only calculate if profit column exists
        if profit_col in df.columns:
            try:
                profit_change = recent_data[profit_col].sum() - prev_data[profit_col].sum()
                profit_change_pct = (profit_change / prev_data[profit_col].sum() * 100) if prev_data[profit_col].sum() != 0 else 0
                if profit_change_pct > 0:
                    insights.append(f"📈 Profit increased by {profit_change_pct:.2f}% this month.")
                else:
                    insights.append(f"📉 Profit dropped by {abs(profit_change_pct):,.2f}% this month. Keep an eye on low-margin products.")
            except Exception as e:
                insights.append(f"Profit insights not available: {e}")

        # Top product - only show if Product column exists
        product_column = st.session_state.column_map.get('Product', 'Product')
        if product_column in df.columns:
            try:
                metric_col = profit_col if profit_col in df.columns else sales_col
                top_product = recent_data.groupby(product_column)[metric_col].sum().idxmax()
                insights.append(f"🏆 Best-selling product: **{top_product}**")
            except Exception:
                pass  # Skip if there's an error with product insights

        # Warning for low sales
        try:
            three_month_avg = df[df['Month'] >= recent_month - 3][sales_col].mean()
            if recent_data[sales_col].sum() < three_month_avg:
                insights.append("⚠️ Sales this month are below the 3-month average. Consider reviewing your strategy.")
        except Exception:
            pass  # Skip if there's an error with sales trend insights

    except Exception as e:
        insights.append(f"Unable to generate some insights: {e}")
        
    # If we couldn't generate any insights, add a generic message
    if not insights:
        insights.append("Not enough data to generate meaningful insights.")

    return insights

# Add Insight Cards section
if st.session_state.get("cleaned_data") is not None:
    df = st.session_state.cleaned_data
    sales_col = st.session_state.column_map.get("Sales")
    profit_col = st.session_state.column_map.get("Profit")
    date_col = st.session_state.column_map.get("Order Date")

    insights = generate_insight_cards(df, date_col, sales_col, profit_col)
    for insight in insights:
        st.info(insight)

show_sidebar_guide()

from helper import handle_missing_columns

if not handle_missing_columns(required_columns=["Order Date", "Sales", "Profit"], optional_columns=["Category", "Region", "Product"]):
    st.stop()