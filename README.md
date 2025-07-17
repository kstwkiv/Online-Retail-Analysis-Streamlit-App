# Online-Retail-Analysis-Streamlit-App
This is a simple Streamlit app that helps you understand your online retail sales data. It shows you the best-selling products, top customers, and suggests items that are often bought together. It's interactive and easy to use!

# Project Overview
This project provides an interactive web application built with Streamlit for analyzing an online retail dataset. It allows users to explore sales trends, identify top-performing products and customers, and get basic product recommendations based on frequently bought together items. The application uses an in-memory SQLite database to run SQL queries directly on the processed data, demonstrating a simple yet powerful way to combine Python data science with SQL analytics in a user-friendly interface.

# Key features
Top Products & Revenue: Identify the top 10 most purchased products by quantity and revenue.

Customer Insights: Discover the top 10 customers based on their purchase volume.

"Frequently Bought Together" Analysis: Explore products commonly purchased alongside a selected item.

Customer-Specific Recommendations: Get personalized product recommendations for individual customers based on their past purchases and frequently bought together patterns.

Interactive UI: User-friendly interface powered by Streamlit for easy navigation and data exploration.

SQL-driven Analytics: Leverages SQL queries (stored externally in queries.sql) for efficient data aggregation and analysis, showcasing SQL integration with Python.

# Technologies used
Python

Streamlit

pandas

SQLite3

Plotly-Express

# Follow these instructions for local setup
Prerequisites:

Python 3.8+
pip

## Installation:
1. clone the repository:
   ```bash
   git clone https://github.com/kstwkiv/Online-Retail-Analysis-Streamlit-App.git
   
   cd Online-Retail-Analysis-Streamlit-App
   ```

3. create a virtual environment:
   ```bash
   python -m venv venv
   #on windows
   .\venv\Scripts\activate
   #on mac
   source venv/bin/activate
   ```

5. install the req packages:
   ```bash
   pip install streamlit pandas plotly
   ```

# Data Source
Place your `OnlineRetail.csv` dataset file directly into the root directory of this project. This application expects the CSV file to be named `OnlineRetail.csv` and encoded in `ISO-8859-1`.

# SQL Queries File
Ensure the  `queries.sql` file (containing all the necessary SQL queries structured with `-- QUERY_NAME` comments) is also placed in the root directory of this project.

# to install the dependencies , follow:
use `pip install -r requirements.txt`

# running the app
1. ensure your virtual environment is active
2. run the streamlit application by using the following command:
   ```bash
   streamlit run app.py
   ```
   this command will open the app in your default browser. usually at https://localhost:8501
