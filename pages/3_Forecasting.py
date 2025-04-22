import streamlit as st
from prophet import Prophet
import plotly.graph_objects as go
from helper import show_sidebar_guide, handle_missing_columns

@st.cache_resource
def compute_forecast(data, months):
    m = Prophet()
    m.fit(data)
    future = m.make_future_dataframe(periods=months * 30)
    return m.predict(future)

if 'selected_currency' not in st.session_state:
    st.session_state.selected_currency = "USD"

st.title("📈 Forecasting")
st.markdown("Using historical data, this page forecasts future **Sales** or **Profit** for the selected number of months.")

# Read data from session state
data = st.session_state.get('cleaned_data', None)
if data is None:
    st.error("No data available. Please upload a file on the Upload page.")
    st.stop()

# Forecast settings
with st.expander("Forecast Settings"):
    months = st.slider("Select number of months to forecast:", 1, 12, 3)
    forecast_metric = st.selectbox("Select Metric to Forecast", ['Sales', 'Profit'])

# Global column map helper
order_date_column = st.session_state.column_map.get('Order Date')

# Check for required columns and provide warnings
if not order_date_column or order_date_column not in data.columns:
    st.warning("Order Date column is missing or not mapped. Forecasting may not be available.")

# Graceful feature skipping
try:
    df_daily = data.groupby(order_date_column).agg({forecast_metric: 'sum'}).reset_index()
    df_daily.columns = ['ds', 'y']

    if df_daily['y'].dropna().shape[0] < 2:
        st.error("Not enough data to forecast. Please upload more data or adjust your filters.")
        st.stop()

    # Perform forecasting
    forecast = compute_forecast(df_daily, months)
    if forecast is None:
        st.stop()

    # Display forecast chart
    st.subheader("Forecast Chart")
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], mode='lines', name='Forecast'))
    fig1.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat_upper'], mode='lines', name='Upper Bound', line=dict(dash='dot')))
    fig1.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat_lower'], mode='lines', name='Lower Bound', line=dict(dash='dot')))
    fig1.update_layout(title='Revenue Forecast (with Confidence Interval)', xaxis_title='Date', yaxis_title=f"{forecast_metric} ({st.session_state.selected_currency})")
    st.plotly_chart(fig1)
except KeyError as e:
    st.info(f"Forecasting couldn't be generated because a required column is missing: {e}")

# Feature requirements badges
st.markdown("### 📅 Forecasting _(requires: Order Date)_")

show_sidebar_guide()

# Display forecast summary
st.subheader("Forecast Summary (Month by Month)")
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
    yaxis_title=f"{forecast_metric} ({st.session_state.selected_currency})",
    showlegend=True
)
st.plotly_chart(fig2)