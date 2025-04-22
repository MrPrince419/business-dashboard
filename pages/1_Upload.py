import streamlit as st
import pandas as pd
from helper import show_sidebar_guide, load_sample_data, reset_session_state
import difflib
from helper import handle_missing_columns, auto_rename_columns

st.title("📤 Upload Your Data")
st.markdown("Upload your sales data here. Supported formats are **CSV** and **Excel**. "
            "The file should include at least columns for order dates, sales, and profit.")

# Ensure session state variables are initialized
if 'cleaned_data' not in st.session_state:
    st.session_state.cleaned_data = None
if 'column_map' not in st.session_state:
    st.session_state.column_map = {}
if 'source' not in st.session_state:
    st.session_state.source = None
if 'selected_currency' not in st.session_state:
    st.session_state.selected_currency = "USD"
if 'rerun_trigger' not in st.session_state:
    st.session_state.rerun_trigger = False

# File upload
file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"], help="Supported formats: CSV, Excel.")

# Add "Use Sample Data" button
if st.button("📊 Use Sample Data"):
    reset_session_state(exclude_keys=['selected_currency'])
    load_sample_data()
    st.success("✅ Sample data loaded successfully. You can now explore all features.")
    # Replace st.experimental_rerun with a workaround
    st.session_state['rerun_trigger'] = not st.session_state.get('rerun_trigger', False)

# Added loading indicator for file processing
with st.spinner("Processing file..."):
    # Enhanced error handling and fallback mechanism for column mapping
    def map_columns(columns, required, optional):
        """Map columns with fallback and user-friendly error handling."""
        mapped_columns = {}
        for col in required:
            matches = difflib.get_close_matches(col, columns, n=1, cutoff=0.4)
            if matches:
                mapped_columns[col] = matches[0]
            else:
                st.warning(f"Required column '{col}' is missing. Please map it manually.")
                mapped_columns[col] = st.selectbox(f"Select column for '{col}'", options=columns, key=f"map_{col}")

        for col in optional:
            matches = difflib.get_close_matches(col, columns, n=1, cutoff=0.4)
            if matches:
                mapped_columns[col] = matches[0]
            else:
                st.info(f"Optional column '{col}' is missing. Related features may be limited.")

        return mapped_columns

    # Automatically clean and preprocess data
    def clean_data(df):
        """Handle missing values and correct common data issues."""
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].fillna('Unknown')  # Fill missing strings with 'Unknown'
        for col in df.select_dtypes(include=['number']).columns:
            df[col] = df[col].fillna(0)  # Fill missing numbers with 0
        for col in df.select_dtypes(include=['datetime']).columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')  # Convert to datetime, handle errors
        return df

    # Process uploaded file
    if file:
        try:
            if file.name.endswith(".csv"):
                df = pd.read_csv(file, encoding_errors='ignore')
            elif file.name.endswith(".xlsx"):
                df = pd.read_excel(file)
            else:
                st.error("Unsupported file type. Please upload a CSV or Excel file.")
                st.stop()

            # Clean and preprocess data
            df = clean_data(df)

            # Auto rename uploaded columns to match expected ones
            required_columns = ["Order Date", "Sales", "Profit", "Product"]
            df = auto_rename_columns(df, required_columns)
            st.session_state.cleaned_data = df

            # Map columns
            required_columns = ["Order Date", "Sales", "Profit"]
            optional_columns = ["Product", "Category"]
            st.session_state.column_map = map_columns(df.columns, required_columns, optional_columns)

            st.success("✅ File processed successfully. You can now explore the data.")
        except Exception as e:
            st.error(f"An error occurred while processing the file: {e}")
            st.stop()

# Add download button for upload template
st.markdown("### 📥 Download Template")
st.download_button(
    label="Download Upload Template",
    data=open("superstore.csv", "rb").read(),
    file_name="upload_template.csv",
    mime="text/csv",
    help="Download a sample template to format your data correctly."
)

# Mapping instruction
st.markdown("### 🗂️ Map Your Columns")
st.markdown("Ensure each selected column matches your dataset structure. "
            "**Order Date** should be the date of each transaction. **Sales** is the amount sold. **Profit** is the net gain.")

# Column mapping UI
if st.session_state.cleaned_data is not None:
    required_columns = ["Order Date", "Sales", "Profit"]
    optional_columns = ["Product", "Product Name", "Category"]

    if not handle_missing_columns(required_columns, optional_columns):
        st.stop()

    data = st.session_state.get("cleaned_data")
    missing_cols = [col for col in required_columns if col not in data.columns]
    if missing_cols:
        st.warning(f"The following column(s) are missing: {', '.join(missing_cols)}. Please upload a complete file or map them correctly.")
        st.stop()

    # Removed redundant column validation logic
    # Updated column mapping logic to rely on fuzzy matching
    columns = st.session_state.cleaned_data.columns

    default_map = {
        "Order Date": difflib.get_close_matches("Order Date", columns, n=1, cutoff=0.6),
        "Sales": difflib.get_close_matches("Sales", columns, n=1, cutoff=0.6),
        "Profit": difflib.get_close_matches("Profit", columns, n=1, cutoff=0.6),
        "Product": difflib.get_close_matches("Product", columns, n=1, cutoff=0.5)
    }

    # Enhanced fallback mechanism for Product column mapping
    product_candidates = [col for col in columns if "product" in col.lower() or "name" in col.lower()]
    if not default_map["Product"] and product_candidates:
        default_map["Product"] = [product_candidates[0]]  # Select the first match as fallback

    # Adjust fuzzy matching threshold for Product
    default_map["Product"] = difflib.get_close_matches("Product", columns, n=1, cutoff=0.4) or default_map["Product"]

    st.session_state.column_map = {
        "Order Date": st.selectbox("Select Order Date Column", options=columns, index=columns.get_loc(default_map["Order Date"][0]) if default_map["Order Date"] else 0),
        "Sales": st.selectbox("Select Sales Column", options=columns, index=columns.get_loc(default_map["Sales"][0]) if default_map["Sales"] else 0),
        "Profit": st.selectbox("Select Profit Column", options=columns, index=columns.get_loc(default_map["Profit"][0]) if default_map["Profit"] else 0),
        "Product": st.selectbox("Select Product Column", options=columns, index=columns.get_loc(default_map["Product"][0]) if default_map["Product"] else 0)
    }

    # Highlight user-selected columns
    st.markdown("### Selected Columns")
    st.write(f"**Order Date Column:** {st.session_state.column_map.get('Order Date', 'Not Mapped')}")
    st.write(f"**Sales Column:** {st.session_state.column_map.get('Sales', 'Not Mapped')}")
    st.write(f"**Profit Column:** {st.session_state.column_map.get('Profit', 'Not Mapped')}")
    st.write(f"**Product Column:** {st.session_state.column_map.get('Product', 'Not Mapped')}")

    # Column Mapping Summary
    st.markdown("### ✅ Column Mapping Summary")

    expected_columns = {
        "Order Date": "Date of transaction (required)",
        "Sales": "Revenue from each order (required)",
        "Profit": "Profit from each order (required)",
        "Category": "Product category (optional, enables filters)",
        "Region": "Customer region (optional, enables filters)",
        "Segment": "Customer segment (optional, enables filters)",
        "Product": "Product name (optional, enables product insights)"
    }

    for col, desc in expected_columns.items():
        mapped = st.session_state.column_map.get(col, None)
        if mapped and mapped in st.session_state.cleaned_data.columns:
            st.success(f"✅ **{col}** mapped to **{mapped}** — {desc}")
        elif col in ["Order Date", "Sales", "Profit"]:
            st.error(f"❌ **{col}** is missing — {desc}")
        else:
            st.warning(f"⚠️ **{col}** not found — {desc}")

# ✅ Show sidebar nav
show_sidebar_guide()