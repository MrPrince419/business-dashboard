import streamlit as st
import pandas as pd

st.title("📤 Upload Your Data")
st.markdown("Upload your sales data here. Supported formats are **CSV** and **Excel**. "
            "The file should include at least columns for order dates, sales, and profit.")

# Ensure session state is initialized
if 'cleaned_data' not in st.session_state:
    st.session_state.cleaned_data = None

# Add file uploader
file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"], help="Supported formats: CSV, Excel. Ensure the file contains valid data.")

# Save uploaded file to session state
if file:
    if file.name.endswith(".csv"):
        df = pd.read_csv(file, encoding_errors='ignore')
    elif file.name.endswith(".xlsx"):
        df = pd.read_excel(file)
    else:
        st.error("Unsupported file type.")
        st.stop()

    st.session_state.cleaned_data = df

# Add instructions for column mapping
st.markdown("### 🗂️ Map Your Columns")
st.markdown("Ensure each selected column matches your dataset structure. "
            "**Order Date** should be the date of each transaction. **Sales** is the amount sold. **Profit** is the net gain.")

# Add sidebar legend for first-time users
st.sidebar.title("🧭 Navigation Guide")
st.sidebar.markdown("- **Upload**: Add your dataset.")
st.sidebar.markdown("- **Dashboard**: View key metrics.")
st.sidebar.markdown("- **Forecasting**: Predict future trends.")
st.sidebar.markdown("- **Profitability**: Analyze profit margins.")
st.sidebar.markdown("- **Anomalies**: Detect revenue spikes/drops.")
st.sidebar.markdown("- **Export**: Download filtered data.")