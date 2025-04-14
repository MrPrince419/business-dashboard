import pandas as pd
import streamlit as st
import datetime
import glob, os
import requests
import pytz  # Re-added pytz for timezone handling

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
def fetch_exchange_rate(base_currency="USD", target_currency="USD"):
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