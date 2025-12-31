import unittest
import pandas as pd
from utils.file_handler import parse_transactions, clean_sales_data

class TestFileHandler(unittest.TestCase):

    def test_parse_valid_lines(self):
        raw_lines = [
            "T001|2024-12-01|P101|Laptop|2|45,000|C001|North",
            "T002|2024-12-02|P102|Mouse,Wireless|5|1,500|C002|South"
        ]
        result = parse_transactions(raw_lines)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["TransactionID"], "T001")
        self.assertEqual(result[0]["ProductName"], "Laptop")
        self.assertEqual(result[0]["Quantity"], 2)
        self.assertEqual(result[0]["UnitPrice"], 45000.0)
        self.assertEqual(result[1]["ProductName"], "MouseWireless")
        self.assertEqual(result[1]["UnitPrice"], 1500.0)

    def test_parse_invalid_lines(self):
        raw_lines = [
            "",  # empty
            "T003|2024-12-03|P103|Keyboard|3|2,000|C003",  # missing Region
            "T004|2024-12-04|P104|Monitor|two|5,000|C004|West",  # invalid Quantity
            "T005|2024-12-05|P105|Webcam|4|abc|C005|East"  # invalid UnitPrice
        ]
        result = parse_transactions(raw_lines)
        self.assertEqual(len(result), 0)

    def test_clean_sales_data(self):
        # Create a small DataFrame with mixed valid/invalid records
        df = pd.DataFrame([
            {"TransactionID": "T001", "Date": "2024-12-01", "ProductID": "P101",
             "ProductName": "Laptop", "Quantity": 2, "UnitPrice": 45000.0,
             "CustomerID": "C001", "Region": "North"},
            {"TransactionID": "X002", "Date": "2024-12-02", "ProductID": "P102",
             "ProductName": "Mouse,Wireless", "Quantity": 5, "UnitPrice": 1500.0,
             "CustomerID": "C002", "Region": "South"},  # invalid TransactionID
            {"TransactionID": "T003", "Date": "2024-12-03", "ProductID": "P103",
             "ProductName": "Keyboard", "Quantity": 0, "UnitPrice": 2000.0,
             "CustomerID": "C003", "Region": "West"}  # invalid Quantity
        ])

        cleaned = clean_sales_data(df)

        # Only the first record should remain valid
        self.assertEqual(len(cleaned), 1)
        self.assertEqual(cleaned.iloc[0]["TransactionID"], "T001")
        self.assertEqual(cleaned.iloc[0]["Revenue"], 90000.0)

if __name__ == "__main__":
    unittest.main()
