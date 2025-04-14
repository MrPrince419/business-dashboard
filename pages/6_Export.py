import streamlit as st
from helper import show_sidebar_guide

if 'selected_currency' not in st.session_state:
    st.session_state.selected_currency = "USD"

st.title("💾 Export Data")
st.markdown("Download the filtered dataset as a CSV file for further analysis or record-keeping.")

# Read data from session state
data = st.session_state.get('cleaned_data', None)
if data is None:
    st.error("No data available. Please upload a file on the Upload page.")
    st.stop()

# Update download button to use session state data
st.download_button("Download Filtered Data as CSV", data=data.to_csv(index=False).encode('utf-8'), file_name="filtered_data.csv", mime="text/csv")

show_sidebar_guide()