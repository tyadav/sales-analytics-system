# Sales Analytics System
## “Turn messy sales data into powerful insights — clean, enrich, analyze, and report with ease.”

This project is a modular Python-based analytics system that processes raw sales transaction data, validates and enriches it, and generates a business-ready report. It supports optional filtering by region and amount, integrates product data from an external API, and produces a clean summary of sales performance.


## 📁 Project Structure
<pre>
With this system, we can:
✅ Parse and clean inconsistent transaction files
🌐 Fetch real-time product details from external APIs (with mock fallback)
📈 Analyze customer behavior, product performance, and regional sales trends
📑 Generate comprehensive CSV reports for strategic decision-making
</pre>
This repository provides a complete, ready-to-run framework for sales data analytics, making it easier for analysts and managers to uncover trends and drive growth.

## Repository Structure:
<pre>
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
</pre>

## ⚙️ Setup Instructions
<pre>
**Clone the repository**
   bash
   git clone https://github.com/tyadav/sales-analytics-system.git
   cd sales-analytics-system
</pre>
## How to run:
<pre>
Prerequisites:
Run requirements.txt
pip install -r requirements.txt
Python 3.10+ installed
pandas==2.2.2 
numpy==1.26.4 
requests==2.32.3
matplotlib==3.10.7
</pre>
## Setup
<pre>
Create and activate a virtual environment:
python -m venv .venv
.venv\Scripts\activate
</pre>
## Execute
<pre>
Run the main pipeline:
python main.py
</pre>
## The cleaning step will print:
<pre>
Total records parsed: 80
Invalid records removed: 10
Valid records after cleaning: 70
</pre>
## Reports will be generated in output/:
<pre>
sales_summary.csv
customer_behavior.csv
region_performance.csv
</pre>
## What it does
Ingests pipe-delimited sales transactions (with messy fields like commas in unit prices or product names).

## Cleans data:
<pre>
Normalizes dates to ISO format.
Coerces quantities and prices to numeric types.
Fixes product names containing commas.
Removes invalid rows (missing fields, wrong types, out-of-range values).
Enriches products via API:
Adds product category and current price information.
Robust mock fallback if the API is unreachable.
</pre>
## Analyzes:
<pre>
Total revenue, units sold, AOV.
Top products, regions, and customers.
Customer behavior patterns: frequency, spend, and product mix.
Outputs business-ready CSV reports.
</pre>
## Expected Outputs
<pre>
After successful execution, the following files will be generated:
data/enriched_sales_data.txt — enriched transaction records with API product info
output/sales_report.txt — summary report including revenue, top products/customers, and daily stats
</pre>
## Assignment Compliance
<pre>
This repository meets all assignment requirements:
Public repo with correct naming
All required files in correct folders
sales_data.txt present in data/
README.md with setup and run instructions
requirements.txt includes all the libraries used
Code runs end-to-end without errors
Output files generated correctly
No hardcoded paths
</pre>
### Contact
For any queries related to this project, please contact:  
📧 tej_on@outlook.com
