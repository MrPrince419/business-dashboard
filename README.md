# 📊 Business Dashboard

## Table of Contents
1. [Overview](#overview)
2. [Problem Statement](#problem-statement)
3. [Data Sources](#data-sources)
4. [Tools & Technologies](#tools--technologies)
5. [Methodology](#methodology)
   - [Data Cleaning / Preprocessing](#1-data-cleaning--preprocessing)
   - [Exploratory Data Analysis (EDA)](#2-exploratory-data-analysis-eda)
   - [Feature Engineering](#3-feature-engineering)
   - [Modeling](#4-modeling)
   - [Validation](#5-validation)
6. [Results & Key Insights](#results--key-insights)
7. [Conclusion & Recommendations](#conclusion--recommendations)
8. [Challenges & Limitations](#challenges--limitations)
9. [Future Work](#future-work)
10. [Appendices](#appendices)
11. [Contact](#contact)
12. [Acknowledgments](#acknowledgments)

---

## Overview
The **Business Dashboard** is an interactive data analytics platform built with Python and Streamlit. It transforms raw business data into actionable insights through advanced visualizations, time-series forecasting, and anomaly detection. Designed for small to medium businesses, this project demonstrates expertise in data processing, exploratory analysis, and predictive modeling.

![Landing Page](asset/landing%20page.png)

---

## Problem Statement
Businesses often struggle to make data-driven decisions due to a lack of accessible tools for analyzing sales, profitability, and trends. This project addresses the need for an easy-to-use platform that provides key performance metrics, forecasts future trends, and identifies anomalies in revenue data.

---

## Data Sources
- **Superstore Dataset**: A publicly available dataset containing sales, profit, and order details. [Download here](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final).
- **Exchange Rate API**: Used for real-time currency conversion. [API Documentation](https://exchangerate-api.com/).

---

## Tools & Technologies
- **Programming Languages**: Python
- **Libraries**: Streamlit, Pandas, Prophet, Plotly, Seaborn, NumPy
- **APIs**: Exchange Rate API
- **Visualization Tools**: Plotly, Seaborn
- **Version Control**: Git
- **Deployment**: Streamlit Cloud

---

## Methodology

### 1. Data Cleaning / Preprocessing
- Handled missing values using configurable imputation methods.
- Automated column mapping with fuzzy matching for consistent schema alignment.
- Standardized currency values using real-time exchange rates.

### 2. Exploratory Data Analysis (EDA)
- Generated descriptive statistics for sales, profit, and order data.
- Visualized trends in revenue, profit margins, and category performance.
- Identified outliers and anomalies in sales data.

#### Revenue Trends
![Revenue Trends](asset/anomalies%20page.png)

### 3. Feature Engineering
- Extracted time-based features (e.g., month, year) for trend analysis.
- Created profitability metrics for product and category comparisons.

#### Profitability by Category
![Profitability by Category](asset/profitability%20page.png)

### 4. Modeling
- Implemented **Facebook Prophet** for time-series forecasting of sales and profit.
- Configured forecast periods (1-12 months) with confidence intervals.

#### Forecasted Sales
![Forecasted Sales](asset/forecasting%20page%20%231.png)

### 5. Validation
- Evaluated forecast accuracy using historical data.
- Visualized residuals to assess model performance.

---

## Results & Key Insights
### Key Metrics
- **Total Revenue**: $2.3M
- **Profit Margin**: 18.5%
- **Top Performing Category**: Technology
- **Lowest Performing Region**: South

---

## Conclusion & Recommendations
### Key Takeaways
- **Revenue Growth**: Consistent growth in Q3 and Q4, driven by the Technology category.
- **Profitability**: Office Supplies have the lowest profit margins and should be re-evaluated.
- **Anomalies**: Detected revenue spikes in December due to seasonal promotions.

### Recommendations
1. Focus marketing efforts on the Technology category to maximize revenue.
2. Investigate and optimize pricing strategies for Office Supplies.
3. Expand operations in the West region, which shows the highest growth potential.

---

## Challenges & Limitations
- **Data Gaps**: Missing values in the Discount and Region columns required imputation.
- **Forecasting Accuracy**: Prophet's performance may vary with limited historical data.
- **Currency Conversion**: Exchange rate API downtime could impact multi-currency analysis.

---

## Future Work
- Integrate additional datasets for customer segmentation and behavior analysis.
- Implement advanced anomaly detection algorithms for real-time monitoring.
- Add support for SQL-based data ingestion to handle larger datasets.

---

## Appendices

### Data Dictionary
| Column Name       | Description                          |
|-------------------|--------------------------------------|
| Order Date        | Date of the order                   |
| Sales             | Total sales amount                  |
| Profit            | Profit earned from the sale         |
| Category          | Product category                    |
| Region            | Geographic region of the sale       |

### Codebase Reference Links
- [Data Cleaning Functions](helper.py)
- [Forecasting Implementation](app.py)
- [Dashboard Pages](pages/)

### External References
- [Facebook Prophet Documentation](https://facebook.github.io/prophet/)
- [Streamlit Documentation](https://docs.streamlit.io/)

---

## Contact
For inquiries or collaboration opportunities, please reach out via:
- **LinkedIn**: [Prince Uwagboe](https://www.linkedin.com/in/prince05/)
- **Email**: [princeuwagboe44@outlook.com](mailto:princeuwagboe44@outlook.com)

---

## Acknowledgments
This project builds upon the foundation of the [Data Analysis Web App](https://github.com/everydaycodings/Data-Analysis-Web-App) with enhancements to analytical capabilities and user interface.
