import os

def read_sales_data(filename):
    """
    Reads sales data from file handling encoding issues.
    Returns: list of raw lines (strings)
    """
    encodings = ["utf-8", "latin-1", "cp1252"]
    for enc in encodings:
        try:
            with open(filename, "r", encoding=enc) as f:
                lines = f.readlines()
                # Skip header and empty lines
                return [line.strip() for line in lines[1:] if line.strip()]
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {filename}")
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError("Unable to decode file with supported encodings.")

def parse_transactions(raw_lines):
    """
    Parses raw lines into clean list of dictionaries.
    """
    transactions = []
    for line in raw_lines:
        parts = line.split("|")
        if len(parts) != 8:
            continue  # skip malformed rows
        try:
            transaction = {
                "TransactionID": parts[0],
                "Date": parts[1],
                "ProductID": parts[2],
                "ProductName": parts[3].replace(",", "").strip(),
                "Quantity": int(parts[4]),
                "UnitPrice": float(parts[5].replace(",", "")),
                "CustomerID": parts[6],
                "Region": parts[7]
            }
            transactions.append(transaction)
        except ValueError:
            continue
    return transactions

def clean_sales_data(df):
    """
    Cleans DataFrame and outputs validation summary.
    """
    total_records = len(df)

    # Drop missing critical fields
    df = df.dropna(subset=["ProductID", "CustomerID", "Region"]).copy()

    # Remove invalid TransactionIDs
    df = df[df["TransactionID"].astype(str).str.startswith("T")].copy()

    # Remove invalid prices and quantities
    df = df[(df["UnitPrice"] > 0) & (df["Quantity"] > 0)].copy()

    # Normalize product names
    df.loc[:, "ProductName"] = df["ProductName"].str.lower().str.replace(",", "").str.strip()

    # Add revenue column
    df.loc[:, "Revenue"] = df["Quantity"] * df["UnitPrice"]

    # Validation summary
    invalid_removed = total_records - len(df)
    summary_text = (
        f"Total records parsed: {total_records}\n"
        f"Invalid records removed: {invalid_removed}\n"
        f"Valid records after cleaning: {len(df)}\n"
    )

    os.makedirs("output", exist_ok=True)
    with open("output/validation_summary.txt", "w", encoding="utf-8") as f:
        f.write(summary_text)

    print(summary_text)
    return df
