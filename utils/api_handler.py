import requests

def fetch_product_info(df):
    """
    Enriches sales DataFrame with product details from Dummy JSON API.
    
    Parameters:
    - df: pandas DataFrame with at least a 'ProductName' column
    
    Returns:
    - pandas DataFrame with new columns: 'brand', 'category', 'description'
    """
    # Get all products from API
    response = requests.get("https://dummyjson.com/products?limit=100")
    data = response.json()
    products = data["products"]

    # Build lookup dictionary by title
    product_lookup = {p["title"]: p for p in products}

    # Map details into DataFrame
    df["brand"] = df["ProductName"].map(lambda name: product_lookup.get(name, {}).get("brand", "Unknown"))
    df["category"] = df["ProductName"].map(lambda name: product_lookup.get(name, {}).get("category", "Unknown"))
    df["description"] = df["ProductName"].map(lambda name: product_lookup.get(name, {}).get("description", ""))

    return df

def fetch_all_products():
    """
    Fetches all products from DummyJSON API.

    Returns:
    - list of product dictionaries with keys:
      id, title, category, brand, price, rating

    Requirements:
    - Fetch all available products (limit=100)
    - Handle connection errors with try-except
    - Return empty list if API fails
    - Print status message (success/failure)
    """
    url = "https://dummyjson.com/products?limit=100"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # raise error for bad status codes
        data = response.json()
        products = data.get("products", [])

        # Extract only required fields
        simplified = [
            {
                "id": p["id"],
                "title": p["title"],
                "category": p["category"],
                "brand": p["brand"],
                "price": p["price"],
                "rating": p["rating"]
            }
            for p in products
        ]

        print(f"✅ Successfully fetched {len(simplified)} products from API")
        return simplified

    except Exception as e:
        print(f"❌ Failed to fetch products: {e}")
        return []

def create_product_mapping(api_products):
    """
    Creates a mapping of product IDs to product info.

    Parameters:
    - api_products: list of product dictionaries from fetch_all_products()

    Returns:
    - dict mapping product IDs to info
    """
    mapping = {
        p["id"]: {
            "title": p["title"],
            "category": p["category"],
            "brand": p["brand"],
            "rating": p["rating"]
        }
        for p in api_products
    }

    return mapping

def enrich_sales_data(transactions, product_mapping):
    """
    Enriches transaction data with API product information.

    Parameters:
    - transactions: list of transaction dictionaries
    - product_mapping: dictionary from create_product_mapping()

    Returns:
    - list of enriched transaction dictionaries
    """
    enriched = []

    for tx in transactions:
        try:
            # Extract numeric ID from ProductID (e.g., P101 -> 101)
            raw_pid = tx.get("ProductID", "")
            numeric_id = None
            if raw_pid.startswith("P"):
                try:
                    numeric_id = int(raw_pid[1:])
                except ValueError:
                    numeric_id = None

            # Lookup product info
            if numeric_id and numeric_id in product_mapping:
                product_info = product_mapping[numeric_id]
                tx["API_Category"] = product_info.get("category")
                tx["API_Brand"] = product_info.get("brand")
                tx["API_Rating"] = product_info.get("rating")
                tx["API_Match"] = True
            else:
                tx["API_Category"] = None
                tx["API_Brand"] = None
                tx["API_Rating"] = None
                tx["API_Match"] = False

            enriched.append(tx)

        except Exception as e:
            # Graceful error handling
            tx["API_Category"] = None
            tx["API_Brand"] = None
            tx["API_Rating"] = None
            tx["API_Match"] = False
            enriched.append(tx)

    # Save enriched data to file
    save_enriched_data(enriched, filename="data/enriched_sales_data.txt")

    return enriched

def save_enriched_data(enriched_transactions, filename="data/enriched_sales_data.txt"):
    """
    Saves enriched transactions back to file in pipe-delimited format.

    Parameters:
    - enriched_transactions: list of enriched transaction dictionaries
    - filename: output file path
    """
    import os

    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # Define header with new fields included
    header = [
        "TransactionID", "Date", "ProductID", "ProductName",
        "Quantity", "UnitPrice", "CustomerID", "Region",
        "API_Category", "API_Brand", "API_Rating", "API_Match"
    ]

    with open(filename, "w", encoding="utf-8") as f:
        # Write header
        f.write("|".join(header) + "\n")

        # Write each transaction
        for tx in enriched_transactions:
            row = []
            for col in header:
                val = tx.get(col)
                if val is None:
                    val = ""  # handle None gracefully
                row.append(str(val))
            f.write("|".join(row) + "\n")

    print(f"✅ Enriched data saved to {filename}")
