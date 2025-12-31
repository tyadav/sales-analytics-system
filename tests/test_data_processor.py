import unittest
import os
import pandas as pd
from utils.data_processor import analyze_sales, generate_report

class TestDataProcessor(unittest.TestCase):
    def setUp(self):
        # Create a small DataFrame for testing
        self.df = pd.DataFrame([
            {"ProductName": "laptop", "Quantity": 2, "UnitPrice": 45000.0, "CustomerID": "C001", "Region": "North"},
            {"ProductName": "mouse", "Quantity": 5, "UnitPrice": 1500.0, "CustomerID": "C002", "Region": "South"},
            {"ProductName": "monitor", "Quantity": 1, "UnitPrice": 10000.0, "CustomerID": "C003", "Region": "West"},
        ])
        self.df["Revenue"] = self.df["Quantity"] * self.df["UnitPrice"]

    def test_generate_report_file(self):
        analysis = analyze_sales(self.df)
        output_path = "output/test_report.txt"

        # Generate report
        generate_report(analysis, output_path)

        # Check file exists
        self.assertTrue(os.path.exists(output_path))

        # Read contents
        with open(output_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Verify sections are present
        self.assertIn("Sales Summary Report", content)
        self.assertIn("Top Products:", content)
        self.assertIn("Top Customers:", content)
        self.assertIn("Regional Sales:", content)

        # Verify product names appear
        self.assertIn("laptop", content)
        self.assertIn("mouse", content)
        self.assertIn("monitor", content)

if __name__ == "__main__":
    unittest.main()
