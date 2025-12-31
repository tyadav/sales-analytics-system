import datetime

def log_run(filters, valid_count, invalid_count, error=None, logfile="output/run_log.csv"):
    """
    Append a log entry to run_log.csv with filter criteria, counts, and errors.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Prepare row
    row = [
        timestamp,
        filters.get("region", ""),
        filters.get("min_amount", ""),
        filters.get("max_amount", ""),
        valid_count,
        invalid_count,
        error if error else ""
    ]

    # Write header if file is new
    try:
        with open(logfile, "x") as f:
            f.write("timestamp,region,min_amount,max_amount,valid_count,invalid_count,error\n")
    except FileExistsError:
        pass

    # Append row
    with open(logfile, "a") as f:
        f.write(",".join(map(str, row)) + "\n")
