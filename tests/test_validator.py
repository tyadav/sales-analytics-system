import unittest
from utils.validator import validate_and_filter

class TestValidationFiltering(unittest.TestCase):
    def test_validation_and_filtering(self):
        transactions = [
            {"TransactionID": "T001", "ProductID": "P101", "CustomerID": "C001", "Quantity": 2, "UnitPrice": 1000, "Region": "North", "Date": "2024-12-01", "ProductName": "Laptop"},
            {"TransactionID": "X002", "ProductID": "P102", "CustomerID": "C002", "Quantity": 0, "UnitPrice": 1500, "Region": "South", "Date": "2024-12-02", "ProductName": "Mouse"},
            {"TransactionID": "T003", "ProductID": "P103", "CustomerID": "C003", "Quantity": 1, "UnitPrice": 500, "Region": "North", "Date": "2024-12-03", "ProductName": "Keyboard"},
        ]

        filtered, invalid_count, summary = validate_and_filter(transactions, region="North", min_amount=1000)

        self.assertEqual(invalid_count, 1)
        self.assertEqual(len(filtered), 1)
        self.assertEqual(summary["filtered_by_region"], 0)
        self.assertEqual(summary["filtered_by_amount"], 1)
        self.assertEqual(summary["final_count"], 1)

if __name__ == "__main__":
    unittest.main()
