import streamlit as st
from helper import show_sidebar_guide

if 'selected_currency' not in st.session_state:
    st.session_state.selected_currency = "USD"

st.title("💾 Export Data")
st.markdown("Download the filtered dataset as a CSV file for further analysis or record-keeping.")

# Read data from session state
data = st.session_state.get('cleaned_data', None)

# Ensure the export functionality works even with incomplete or partially cleaned data
if data is None or data.empty:
    st.error("No data available to export. Please upload a file and process it first.")
    st.stop()

# Graceful feature skipping
try:
    # Update download button to use session state data
    st.download_button("Download Filtered Data as CSV", data=data.to_csv(index=False).encode('utf-8'), file_name="filtered_data.csv", mime="text/csv")
except Exception as e:
    st.info(f"Export functionality couldn't be completed due to an error: {e}")

# Feature requirements badges
st.markdown("### 💾 Export Data _(requires: Processed Data)_")

show_sidebar_guide()