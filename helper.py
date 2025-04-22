import pandas as pd
import streamlit as st
import datetime
import glob, os
import requests
import pytz  # Re-added pytz for timezone handling
import pickle
from typing import Optional, Dict
import difflib

excel_type =["vnd.ms-excel","vnd.openxmlformats-officedocument.spreadsheetml.sheet", "vnd.oasis.opendocument.spreadsheet", "vnd.oasis.opendocument.text"]

def match_elements(list_a, list_b):
    non_match = []
    for i in list_a:
        if i  in list_b:
            non_match.append(i)
    return non_match

def download_data(data, label):
    current_time = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
    current_time = "{}.{}-{}-{}".format(current_time.date(), current_time.hour, current_time.minute, current_time.second)
    export_data = st.download_button(
                        label="Download {} data as CSV".format(label),
                        data=data.to_csv(),
                        file_name='{}{}.csv'.format(label, current_time),
                        mime='text/csv',
                        help = "When You Click On Download Button You can download your {} CSV File".format(label)
                    )
    return export_data

def describe(data):
    global num_category, str_category
    num_category = [feature for feature in data.columns if data[feature].dtypes != "O"]
    str_category = [feature for feature in data.columns if data[feature].dtypes == "O"]
    column_with_null_values = data.columns[data.isnull().any()]
    return data.describe(), data.shape, data.columns, num_category, str_category, data.isnull().sum(),data.dtypes.astype("str"), data.nunique(), str_category, column_with_null_values

def drop_items(data, selected_name):
    droped = data.drop(selected_name, axis = 1)
    return droped

def rename_columns(data, column_names):
    rename_column = data.rename(columns=column_names)
    return rename_column

def handling_missing_values(data, option_type, dict_value=None):
    if option_type == "Drop all null value rows":
        data = data.dropna()

    elif option_type == "Only Drop Rows that contanines all null values":
        data = data.dropna(how="all")
    
    elif option_type == "Filling in Missing Values":
        data = data.fillna(dict_value)
    
    return data

def clear_image_cache():
    removing_files = glob.glob('temp/*.png')
    for i in removing_files:
        os.remove(i)

# Function to fetch exchange rates from a free API
@st.cache_data(ttl=3600)  # Cache for 1 hour
def fetch_exchange_rate(base_currency: str = "USD", target_currency: str = "USD") -> float:
    """Fetch exchange rates from a free API."""
    try:
        response = requests.get(f"https://api.exchangerate-api.com/v4/latest/{base_currency}")
        if response.status_code == 200:
            rates = response.json().get("rates", {})
            return rates.get(target_currency, 1.0)  # Default to 1.0 if target currency not found
        else:
            st.warning("Failed to fetch exchange rates. Using default rate of 1.0.")
            return 1.0
    except Exception as e:
        st.error(f"Error fetching exchange rate: {e}")
        return 1.0

def show_sidebar_guide():
    st.sidebar.title("🧭 Navigation Guide")
    st.sidebar.markdown("- **Upload**: Add your dataset.")
    st.sidebar.markdown("- **Dashboard**: View key metrics.")
    st.sidebar.markdown("- **Forecasting**: Predict future trends.")
    st.sidebar.markdown("- **Profitability**: Analyze profit margins.")
    st.sidebar.markdown("- **Anomalies**: Detect revenue spikes/drops.")
    st.sidebar.markdown("- **Export**: Download filtered data.")
    st.sidebar.markdown("- **Help**: View FAQs and instructions.")
    st.sidebar.markdown("---")
    st.sidebar.markdown("🙋 Have suggestions?")
    st.sidebar.markdown("[Send Feedback](https://formspree.io/f/moverold)")

# Store column map in session file
def save_session_state():
    with open("session_state.pkl", "wb") as f:
        pickle.dump(st.session_state.column_map, f)

def load_session_state():
    try:
        with open("session_state.pkl", "rb") as f:
            st.session_state.column_map = pickle.load(f)
    except FileNotFoundError:
        st.session_state.column_map = {}

def load_sample_data():
    """Load the sample data and set the column map."""
    try:
        sample_data = pd.read_csv("superstore.csv", encoding="utf-8", on_bad_lines='skip')
        st.session_state.cleaned_data = sample_data.copy()
        st.session_state.column_map = {
            "Order Date": "Order Date",
            "Sales": "Sales",
            "Profit": "Profit",
        }
        st.session_state.source = "sample"
    except UnicodeDecodeError:
        try:
            sample_data = pd.read_csv("superstore.csv", encoding="ISO-8859-1")
            st.session_state.cleaned_data = sample_data.copy()
            st.session_state.column_map = {
                "Order Date": "Order Date",
                "Sales": "Sales",
                "Profit": "Profit",
            }
            st.session_state.source = "sample"
        except Exception as e:
            st.error(f"Error loading sample data: {e}. Please ensure the file is properly encoded.")
    except FileNotFoundError:
        st.error("Sample data file not found. Please ensure 'superstore.csv' exists in the project directory.")
    except pd.errors.ParserError as e:
        st.error(f"Error parsing sample data: {e}. Please check the file for formatting issues.")
    except Exception as e:
        st.error(f"Unexpected error loading sample data: {e}")

def reset_session_state(exclude_keys=None):
    """Reset all session state except for specified keys."""
    if exclude_keys is None:
        exclude_keys = []
    for key in list(st.session_state.keys()):
        if key not in exclude_keys:
            del st.session_state[key]

def handle_missing_columns(required_columns, optional_columns=None):
    """Check for missing columns in the uploaded data."""
    data = st.session_state.get("cleaned_data")
    if data is None:
        return False

    missing = [col for col in required_columns if col not in data.columns]
    optional_missing = []

    if optional_columns:
        optional_missing = [col for col in optional_columns if col not in data.columns]

    if missing:
        st.warning(f"The following required column(s) are missing: {', '.join(missing)}.")
        return False

    if optional_missing:
        st.info(f"The following optional column(s) are missing and related features may be limited: {', '.join(optional_missing)}.")

    return True

def auto_rename_columns(df, required_columns):
    """
    Auto-renames columns in the DataFrame to match the required columns using fuzzy matching.
    """
    renamed_columns = {}
    for required in required_columns:
        best_match = difflib.get_close_matches(required, df.columns, n=1, cutoff=0.6)
        if best_match:
            renamed_columns[best_match[0]] = required
    df = df.rename(columns=renamed_columns)
    return df

def generate_summary(data, column_map):
    try:
        sales_col = column_map.get("Sales")
        profit_col = column_map.get("Profit")
        date_col = column_map.get("Order Date")
        product_col = column_map.get("Product", None)
        region_col = column_map.get("Region", None)

        # Ensure date is datetime
        data[date_col] = pd.to_datetime(data[date_col], errors="coerce")
        latest_month = data[date_col].dt.to_period("M").max()
        prev_month = latest_month - 1

        monthly = data.copy()
        monthly["Month"] = data[date_col].dt.to_period("M")
        current = monthly[monthly["Month"] == latest_month]
        previous = monthly[monthly["Month"] == prev_month]

        # Revenue comparison
        rev_now = current[sales_col].sum()
        rev_prev = previous[sales_col].sum()
        rev_growth = ((rev_now - rev_prev) / rev_prev * 100) if rev_prev else 0

        # Profit margin
        prof_now = current[profit_col].sum()
        margin = (prof_now / rev_now * 100) if rev_now else 0

        # Top product
        top_product = None
        if product_col and product_col in data.columns:
            top_product = (
                current.groupby(product_col)[sales_col].sum().idxmax()
                if not current.empty else None
            )

        # Weakest region (optional)
        worst_region = None
        if region_col and region_col in data.columns:
            worst_region = (
                current.groupby(region_col)[sales_col].sum().idxmin()
                if not current.empty else None
            )

        summary = f"Revenue {'increased' if rev_growth > 0 else 'decreased'} {abs(rev_growth):.1f}% month-over-month. "
        summary += f"Profit margin: {margin:.1f}%. "
        if top_product:
            summary += f"Top product: *{top_product}*. "
        if worst_region:
            summary += f"Slowest region: *{worst_region}*."

        return summary
    except Exception as e:
        return f"Could not generate summary: {e}"

# Call load_session_state at the start of the app
load_session_state()