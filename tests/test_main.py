import unittest
import os
import subprocess

class TestMainIntegration(unittest.TestCase):
    def test_pipeline_end_to_end(self):
        # Run main.py as a subprocess
        result = subprocess.run(
            ["python", "main.py"],
            capture_output=True,
            text=True
        )

        # Ensure main.py ran without crashing
        self.assertEqual(result.returncode, 0)

        # Check that output files exist
        self.assertTrue(os.path.exists("output/report.txt"))
        self.assertTrue(os.path.exists("output/validation_summary.txt"))

        # Read validation summary
        with open("output/validation_summary.txt", "r", encoding="utf-8") as f:
            validation_content = f.read()
        self.assertIn("Total records parsed", validation_content)
        self.assertIn("Invalid records removed", validation_content)
        self.assertIn("Valid records after cleaning", validation_content)

        # Read report
        with open("output/report.txt", "r", encoding="utf-8") as f:
            report_content = f.read()
        self.assertIn("Sales Summary Report", report_content)
        self.assertIn("Top Products:", report_content)
        self.assertIn("Top Customers:", report_content)
        self.assertIn("Regional Sales:", report_content)

if __name__ == "__main__":
    unittest.main()
