# 📊 Business Dashboard

## Overview
A data analytics platform built with Python and Streamlit that transforms business data into actionable insights through interactive visualizations, time-series forecasting, and anomaly detection. This dashboard is designed for small to medium businesses who need effective analytics without enterprise-level complexity.

## Core Analytics Capabilities

### Data Processing & Transformation
- **Multi-format Ingestion**: Supports CSV and Excel files with automated column detection
- **Data Cleaning Pipeline**: Handles missing values through configurable imputation methods
- **Column Mapping**: Smart column name mapping with fuzzy matching
- **Currency Conversion**: Exchange rate integration for multi-currency analysis

### Visualization & Metrics
- **Interactive KPI Dashboard**: 
  - Total Revenue, Profit, Average Order Value
  - Month-over-month performance metrics
  - Time-series visualization with date range filtering
- **Data Summary**: Automated analysis with descriptive statistics
- **Trend Identification**: Visual highlighting of performance changes

### Advanced Analytics
- **Time Series Forecasting**: 
  - Implementation of Facebook Prophet algorithm
  - Configurable forecast periods (1-12 months)
  - Confidence intervals visualization
  - Month-by-month forecast summaries
- **Profitability Analysis**:
  - Product/category profit margin calculations
  - Performance rankings and comparisons
- **Anomaly Detection**:
  - Statistical pattern analysis in revenue data
  - Visual highlighting of potential anomalies

### Data Export & Reporting
- **Customizable Exports**: Filter and download data in CSV format
- **Timestamped Files**: Automatic date and time stamping of exports

## Technical Implementation

### Architecture
- **Modular Design**: Separate pages for different analytical functions
- **Session State Management**: Persistent data between page navigation
- **Caching**: Strategic implementation of Streamlit's caching for performance

### Technology Stack
- **Frontend & Visualization**: 
  - Streamlit for UI components and interactivity
  - Plotly for dynamic, interactive charts
- **Data Processing**:
  - Pandas for data manipulation and analysis
  - Prophet for time series forecasting
- **External Integrations**:
  - Exchange rate API for currency conversion

## Application Interface

![Landing Page](asset/landing%20page.png)
*The landing page provides an overview of capabilities and navigation instructions*

### Module Breakdown

| Module | Analytical Capabilities | Interface Preview |
|--------|-------------------------|-------------------|
| **Upload & Processing** | • Data validation<br>• Column mapping<br>• Missing value handling | ![Upload](asset/upload%20page%20%231.png) |
| **Dashboard** | • Key performance metrics<br>• Time-series visualization<br>• Filterable views | ![Dashboard](asset/dashboard%20page%20%231.png) |
| **Forecasting** | • Prophet forecasting<br>• Configurable periods (1-12 months)<br>• Confidence intervals | ![Forecasting](asset/forecasting%20page%20%231.png) |
| **Profitability** | • Margin analysis<br>• Product performance<br>• Category comparison | ![Profitability](asset/profitability%20page.png) |
| **Anomaly Detection** | • Pattern analysis<br>• Revenue spike detection<br>• Visual highlighting | ![Anomalies](asset/anomalies%20page.png) |
| **Export** | • Filtered data downloads<br>• CSV format with timestamps | ![Export](asset/export%20page.png) |
| **Help** | • Feature explanations<br>• Usage guidance | ![Help](asset/help%20page%20%231.png) |

## Installation & Setup

### System Requirements
- Python 3.8+
- Modern web browser with JavaScript enabled

### Dependencies
```
streamlit
pandas
prophet
plotly
openpyxl
pytz
requests
```
Full requirements available in `requirements.txt`

### Installation Steps

```bash
# Clone repository
git clone https://github.com/your-repo/business-dashboard.git
cd business-dashboard

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Launch application
streamlit run app.py
```

### Sample Data
The repository includes `superstore.csv` as a sample dataset that demonstrates functionality without requiring initial data upload.

## Usage Examples

### Sales Forecasting Workflow
1. Upload sales data with Order Date and Sales columns
2. Navigate to Forecasting page
3. Select forecast period (1-12 months)
4. Choose metric to forecast (Sales or Profit)
5. View forecast chart with confidence intervals
6. Analyze month-by-month forecast summary

### Profitability Analysis Workflow
1. Ensure data contains product, sales and profit information
2. Navigate to Profitability page
3. View calculated profit margins
4. Filter time periods as needed
5. Export filtered data for further analysis

## Live Demo & Resources

- **Live Application**: [Business Dashboard](https://bussiness-dashboard.streamlit.app/)
- **Source Code**: [GitHub Repository](https://github.com/everydaycodings/Data-Analysis-Web-App)

## Deployment Options

- **Streamlit Cloud**: [![Deploy on Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io/)
- **Alternative Options**:
  - [Render](https://render.com/)
  - [Railway](https://railway.app/)

## Acknowledgments

This project builds upon the foundation of the [Data Analysis Web App](https://github.com/everydaycodings/Data-Analysis-Web-App) with enhancements to analytical capabilities and user interface.
