import streamlit as st
from helper import show_sidebar_guide
import requests

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

# Added a collapsible FAQ section
with st.expander("Frequently Asked Questions"):
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

# Update Help page with new instructions
st.markdown("### 🆘 Help & FAQs")
st.markdown("""
- **Use Sample Data**: If you don't have your own file, click the 'Use Sample Data' button on the Upload page.
- **Column Mapping**: Map your dataset's columns to the required fields (Order Date, Sales, Profit) using the dropdowns.
- **Missing Columns**: If any required columns are missing, the app will warn you and skip the affected features.
""")

st.markdown("### Frequently Asked Questions")
st.markdown("""
**What if my data has missing columns?**
Don't worry — we'll show a warning and continue. Use the "Map Columns" section to fix mismatches.

**Can I customize columns like 'Profit'?**
Yes, just upload your file and map it using the dropdowns.
""")

st.markdown("### 💬 Got Feedback?")
st.write("We'd love to hear your thoughts, ideas, or issues.")

# Embed Formspree feedback form directly in the app with proper form submission
with st.form("feedback_form"):
    email = st.text_input("Your Email", placeholder="Your email", key="feedback_email")
    feedback = st.text_area("Your Feedback", placeholder="Your feedback here...", key="feedback_message")
    submitted = st.form_submit_button("Submit Feedback")

    # Actually submit the form to Formspree when the button is clicked
    if submitted:
        if email and feedback:
            # Submit to Formspree
            form_data = {
                "email": email,
                "message": feedback
            }
            response = requests.post(
                "https://formspree.io/f/moverold",
                data=form_data
            )
            
            if response.status_code == 200:
                st.success("Thank you for your feedback! We'll get back to you soon.")
            else:
                st.error(f"There was an error submitting your feedback. Please try again later. (Error: {response.status_code})")
        else:
            st.error("Please fill out both the email and feedback fields before submitting.")