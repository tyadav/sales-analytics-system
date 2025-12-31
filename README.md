# Sales Analytics System
Python Programming Assignment - Sales Analytics System
## “Turn messy sales data into powerful insights — clean, enrich, analyze, and report with ease.”

The Sales Analytics System is a Python-based solution designed for e-commerce companies to transform raw, messy sales data into actionable business insights. It automates the process of data cleaning, API integration for product enrichment, sales pattern analysis, and report generation.

With this system, we can:
✅ Parse and clean inconsistent transaction files
🌐 Fetch real-time product details from external APIs (with mock fallback)
📈 Analyze customer behavior, product performance, and regional sales trends
📑 Generate comprehensive CSV reports for strategic decision-making

This repository provides a complete, ready-to-run framework for sales data analytics, making it easier for analysts and managers to uncover trends and drive growth.

# Repository Structure:

sales-analytics-system/
  ├── README.md
  ├── main.py
  ├── utils/
  │   ├── file_handler.py
  │   ├── data_processor.py
  │   └── api_handler.py
  ├── data/
  │   └── sales_data.txt
  ├── output/
  └── requirements.txt

# How to run
Prerequisites
Run requirements.txt
Python 3.10+ installed
pandas==2.2.2 
numpy==1.26.4 
requests==2.32.3
matplotlib==3.10.7

# Setup
Create and activate a virtual environment:
python -m venv .venv
.venv\Scripts\activate

# Install dependencies:
pip install -r requirements.txt

# Execute
Run the main pipeline:
python main.py

# The cleaning step will print:
Total records parsed: 80
Invalid records removed: 10
Valid records after cleaning: 70

# Reports will be generated in output/:
sales_summary.csv
customer_behavior.csv
region_performance.csv

# What it does
Ingests pipe-delimited sales transactions (with messy fields like commas in unit prices or product names).

# Cleans data:
Normalizes dates to ISO format.
Coerces quantities and prices to numeric types.
Fixes product names containing commas.
Removes invalid rows (missing fields, wrong types, out-of-range values).
Enriches products via API:
Adds product category and current price information.
Robust mock fallback if the API is unreachable.

# Analyzes:
Total revenue, units sold, AOV.
Top products, regions, and customers.
Customer behavior patterns: frequency, spend, and product mix.
Outputs business-ready CSV reports.

## Contact
For any queries related to this project, please contact:  
📧 tej_on@outlook.com
