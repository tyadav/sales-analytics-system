import os
import sys
import pandas as pd

from utils.file_handler import read_sales_data, parse_transactions, clean_sales_data
from utils.validator import validate_transactions
from utils.logger import log_run
from utils.api_handler import (
    fetch_all_products,
    create_product_mapping,
    enrich_sales_data,
)
from utils.data_processor import (
    calculate_total_revenue,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products,
    generate_sales_report,
    generate_daily_sales_chart,
    average_order_value,
    region_performance,
    top_products,
    top_customers,
    daily_sales_stats,
)


def safe_input(prompt: str) -> str:
    """Handle interactive input safely and exit on interrupt."""
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        print("\nInput cancelled. Exiting.")
        sys.exit(0)


def ensure_df(obj, columns=None):
    """Normalize various return types into a pandas DataFrame."""
    if isinstance(obj, pd.DataFrame):
        return obj.copy()
    if obj is None:
        return pd.DataFrame(columns=columns) if columns else pd.DataFrame()
    if isinstance(obj, dict):
        try:
            return pd.DataFrame.from_dict(obj, orient="index")
        except Exception:
            return pd.DataFrame([obj])
    try:
        return pd.DataFrame(obj)
    except Exception:
        return pd.DataFrame(columns=columns) if columns else pd.DataFrame()


def main():
    """
    Main execution function for Sales Analytics System.
    This version omits chart and Excel generation per assignment requirements.
    """
    os.makedirs("output", exist_ok=True)
    os.makedirs("data", exist_ok=True)

    print("======================================================")
    print("                 SALES ANALYTICS SYSTEM              " )
    print("======================================================\n")

    filters = {"region": "", "min_amount": "", "max_amount": ""}

    try:
        # [1/10] Read sales data
        print("[1/10] Reading sales data...")
        raw_data = read_sales_data("data/sales_data.txt")
        print(f"✓ Successfully read {len(raw_data)} transactions\n")

        # [2/10] Parse and clean
        print("[2/10] Parsing and cleaning data...")
        parsed = parse_transactions(raw_data)
        print(f"✓ Parsed {len(parsed)} records\n")

        # [3/10] Filter Options
        print("[3/10] Filter Options Available:")
        regions = sorted(set(tx.get("Region", "") for tx in parsed if tx.get("Region")))
        amounts = []
        for tx in parsed:
            try:
                amounts.append(float(tx.get("UnitPrice", 0)))
            except (TypeError, ValueError):
                pass

        if regions:
            print(f"Regions: {', '.join(regions)}")
        else:
            print("Regions: No transactions available")

        if amounts:
            print(f"Amount Range: ₹{min(amounts):.2f} - ₹{max(amounts):.2f}\n")
        else:
            print("Amount Range: No transactions available\n")

        # Retry loop if filters leave no records
        while True:
            choice = safe_input("Do you want to filter data? (y/n): ").strip().lower()
            if choice not in ("y", "n"):
                print("Please enter 'y' or 'n'.")
                continue

            if choice == "y":
                region_choice = safe_input("Enter region to filter (or press Enter to skip): ").strip()
                min_amt = safe_input("Enter minimum amount (or press Enter to skip): ").strip()
                max_amt = safe_input("Enter maximum amount (or press Enter to skip): ").strip()

                filters = {
                    "region": region_choice,
                    "min_amount": min_amt,
                    "max_amount": max_amt,
                }

                filtered = parsed

                if region_choice:
                    filtered = [
                        tx for tx in filtered
                        if tx.get("Region", "").lower() == region_choice.lower()
                    ]

                if min_amt:
                    try:
                        min_val = float(min_amt)
                        filtered = [
                            tx for tx in filtered
                            if float(tx.get("UnitPrice", 0)) >= min_val
                        ]
                    except ValueError:
                        print("⚠️ Invalid minimum amount. Ignoring.")

                if max_amt:
                    try:
                        max_val = float(max_amt)
                        filtered = [
                            tx for tx in filtered
                            if float(tx.get("UnitPrice", 0)) <= max_val
                        ]
                    except ValueError:
                        print("⚠️ Invalid maximum amount. Ignoring.")

                parsed = filtered
                print(f"✓ Filter applied, {len(parsed)} records remain\n")

                if not parsed:
                    print("⚠️ No transactions match the filter criteria.")
                    retry = safe_input("Would you like to try different filters? (y/n): ").strip().lower()
                    if retry == "y":
                        continue
                    else:
                        print("Exiting workflow.")
                        log_run(filters, valid_count=0, invalid_count=0, error="No transactions after filter")
                        return
                else:
                    break
            else:
                print("✓ No filter applied\n")
                break

        # [4/10] Validate transactions
        print("[4/10] Validating transactions...")
        valid, invalid = validate_transactions(parsed)
        print(f"✓ Valid: {len(valid)} | Invalid: {len(invalid)}\n")

        # [5/10] Analyzing sales data
        print("[5/10] Analyzing sales data...")

        if not valid:
            print("⚠️ No valid transactions to analyze.")
            analysis = {
                "total_revenue": 0.0,
                "average_order_value": 0.0,
                "region_performance": pd.DataFrame(columns=["Region", "Revenue"]),
                "top_products": pd.DataFrame(columns=["Product", "Quantity", "Revenue"]),
                "top_customers": pd.DataFrame(columns=["Customer", "Revenue"]),
                "daily_sales_stats": pd.DataFrame(columns=["Date", "Revenue", "Transactions"]),
                "low_performing_products": pd.DataFrame(columns=["Product", "Quantity", "Revenue"]),
                "product_summary": pd.DataFrame(columns=["Product", "Quantity", "Revenue", "Type"]),
            }
        else:
            total_revenue_value = calculate_total_revenue(valid)
            average_order_value_value = average_order_value(valid)

            # Ensure helper functions are callable
            helpers = {
                "region_performance": region_performance,
                "top_products": top_products,
                "top_customers": top_customers,
                "daily_sales_stats": daily_sales_stats,
                "low_performing_products": low_performing_products,
            }
            for name, func in helpers.items():
                if not callable(func):
                    raise RuntimeError(f"Helper function '{name}' is not callable or has been shadowed.")

            region_stats_df = ensure_df(region_performance(valid))
            product_stats_df = ensure_df(top_products(valid))
            customer_stats_df = ensure_df(top_customers(valid))
            daily_stats_df = ensure_df(daily_sales_stats(valid))

            low_perf_raw = low_performing_products(valid)
            if low_perf_raw:
                try:
                    low_perf_df = pd.DataFrame(low_perf_raw, columns=["Product", "Quantity", "Revenue"])
                except Exception:
                    low_perf_df = ensure_df(low_perf_raw)
            else:
                low_perf_df = pd.DataFrame(columns=["Product", "Quantity", "Revenue"])

            try:
                product_summary_df = pd.concat([
                    product_stats_df.assign(Type="Top"),
                    low_perf_df.assign(Type="Low")
                ], ignore_index=True, sort=False)
            except Exception:
                product_summary_df = pd.DataFrame(columns=["Product", "Quantity", "Revenue", "Type"])

            analysis = {
                "total_revenue": total_revenue_value,
                "average_order_value": average_order_value_value,
                "region_performance": region_stats_df,
                "top_products": product_stats_df,
                "top_customers": customer_stats_df,
                "daily_sales_stats": daily_stats_df,
                "low_performing_products": low_perf_df,
                "product_summary": product_summary_df,
            }

        print("✓ Analysis complete\n")

        log_run(filters, len(valid), len(invalid))

        # [6/10] Fetch products from API
        print("[6/10] Fetching product data from API...")
        try:
            api_products = fetch_all_products()
            print(f"✓ Fetched {len(api_products)} products\n")
        except Exception as api_err:
            api_products = []
            print(f"❌ Failed to fetch products: {api_err}")
            print("✓ Fetched 0 products\n")

        # [7/10] Enrich sales data
        print("[7/10] Enriching sales data...")
        product_map = create_product_mapping(api_products)
        enriched = enrich_sales_data(valid, product_map)
        enriched_count = sum(1 for tx in enriched if tx.get("API_Match"))
        success_rate = (enriched_count / len(enriched) * 100) if enriched else 0

        enriched_path = "data/enriched_sales_data.txt"
        try:
            with open(enriched_path, "w", encoding="utf-8") as f:
                for tx in enriched:
                    f.write(str(tx) + "\n")
            print("✅ Enriched data saved to data/enriched_sales_data.txt")
        except Exception as save_err:
            print(f"⚠️ Failed to save enriched data: {save_err}")

        print(f"✓ Enriched {enriched_count}/{len(enriched)} transactions ({success_rate:.1f}%)\n")

        # [8/10] Saving enriched data
        print("[8/10] Saving enriched data...")
        print("✓ Saved to: data/enriched_sales_data.txt\n")

        # Show analysis contents and types
        print("\n--- Analysis contents ---")
        for key, value in analysis.items():
            print(f"{key}: {type(value)}")

        # [9/10] Generate report
        print("[9/10] Generating report...")
        if not valid:
            print("⚠️ No valid transactions, skipping report generation.\n")
        else:
            generate_sales_report(valid, enriched, output_file="output/sales_report.txt")
            print("✅ Sales report generated at output/sales_report.txt")
            print("✓ Report saved to: output/sales_report.txt\n")

        # [10/10] Charts and Excel export omitted per assignment
        print("[10/10] Charts and Excel export omitted per assignment requirements\n")

        # Additional outputs

        total_rev_value = calculate_total_revenue(valid)
        print(f"\nTotal Revenue: ₹{total_rev_value:.2f}")

        daily_trend = daily_sales_trend(enriched)
        print("\nDaily Sales Trend:")
        if isinstance(daily_trend, dict) and daily_trend:
            for date, stats in daily_trend.items():
                print(
                    f"{date}: Revenue=₹{stats.get('revenue', 0):.2f}, "
                    f"Transactions={stats.get('transaction_count', 0)}, "
                    f"Unique Customers={stats.get('unique_customers', 0)}"
                )
        else:
            print("No daily trend data available.")

        peak_day = find_peak_sales_day(enriched)
        if peak_day:
            print(f"\nPeak Sales Day: {peak_day[0]} | Revenue=₹{peak_day[1]:.2f}, Transactions={peak_day[2]}")
        else:
            print("\nPeak Sales Day: No data")

        low_products_enriched = low_performing_products(enriched, threshold=10)
        print("\nLow Performing Products (enriched view):")
        if low_products_enriched:
            for pname, qty, revenue in low_products_enriched:
                print(f"{pname}: Quantity={qty}, Revenue=₹{revenue:.2f}")
        else:
            print("No low performing products found (enriched view).")

        def safe_head(df):
            return df.head() if isinstance(df, pd.DataFrame) else df

        print("\nRegion Performance (DF head):\n", safe_head(analysis.get("region_performance")))
        print("\nTop Products (DF head):\n", safe_head(analysis.get("top_products")))
        print("\nTop Customers (DF head):\n", safe_head(analysis.get("top_customers")))
        print("\nDaily Sales Stats (DF head):\n", safe_head(analysis.get("daily_sales_stats")))
        print("\nLow Performing Products (DF head):\n", safe_head(analysis.get("low_performing_products")))
        print("\nProduct Summary (DF head):\n", safe_head(analysis.get("product_summary")))

    except Exception as e:
        try:
            log_run(
                filters if isinstance(filters, dict) else {},
                len(locals().get("valid", [])),
                len(locals().get("invalid", [])),
                error=str(e),
            )
        except Exception:
            pass

        print("❌ An error occurred during execution.")
        print(f"Error details: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
