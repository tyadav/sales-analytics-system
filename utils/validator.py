def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validates transactions and applies optional filters.
    Returns: (valid_transactions, invalid_count, filter_summary)
    """
    required_fields = ["TransactionID", "Date", "ProductID", "ProductName",
                       "Quantity", "UnitPrice", "CustomerID", "Region"]

    valid = []
    invalid_count = 0

    # Step 1: Validation
    for tx in transactions:
        if not all(field in tx for field in required_fields):
            invalid_count += 1
            continue
        if not (str(tx["TransactionID"]).startswith("T") and
                str(tx["ProductID"]).startswith("P") and
                str(tx["CustomerID"]).startswith("C")):
            invalid_count += 1
            continue
        if tx["Quantity"] <= 0 or tx["UnitPrice"] <= 0:
            invalid_count += 1
            continue
        valid.append(tx)

    # Step 2: Print available regions and amount range
    regions = sorted(set(tx["Region"] for tx in valid))
    amounts = [tx["Quantity"] * tx["UnitPrice"] for tx in valid]
    print(f"Available regions: {regions}")
    print(f"Transaction amount range: ₹{min(amounts):.2f} to ₹{max(amounts):.2f}")

    # Step 3: Filtering
    filtered = valid.copy()
    filtered_by_region = 0
    filtered_by_amount = 0

    if region:
        before = len(filtered)
        filtered = [tx for tx in filtered if tx["Region"] == region]
        filtered_by_region = before - len(filtered)
        print(f"Filtered by region '{region}': {filtered_by_region} removed")

    if min_amount is not None or max_amount is not None:
        before = len(filtered)
        filtered = [
            tx for tx in filtered
            if (min_amount is None or tx["Quantity"] * tx["UnitPrice"] >= min_amount) and
               (max_amount is None or tx["Quantity"] * tx["UnitPrice"] <= max_amount)
        ]
        filtered_by_amount = before - len(filtered)
        print(f"Filtered by amount: {filtered_by_amount} removed")

    # Step 4: Summary
    summary = {
        "total_input": len(transactions),
        "invalid": invalid_count,
        "filtered_by_region": filtered_by_region,
        "filtered_by_amount": filtered_by_amount,
        "final_count": len(filtered)
    }

    return filtered, invalid_count, summary

def validate_transactions(transactions):
    """
    Validates transactions by checking for positive Quantity and UnitPrice.
    Splits transactions into valid and invalid lists.
    Valid = Quantity > 0 and UnitPrice > 0
    Returns: (valid, invalid)
    """
    valid = []
    invalid = []

    for tx in transactions:
        qty = tx.get("Quantity", 0)
        price = tx.get("UnitPrice", 0)

        if qty > 0 and price > 0:
            valid.append(tx)
        else:
            invalid.append(tx)

    return valid, invalid


