import csv
import os
import random
import decimal # Use decimal for precise financial calculations

# --- Configuration ---
# No input path needed as we are creating a new file
OUTPUT_CSV_PATH = 'static/output_updated.csv'
TARGET_ROW_COUNT = 3000
MIN_BALANCE = decimal.Decimal('10000.00')
MAX_BALANCE = decimal.Decimal('110000.00') # Exclusive upper bound for random.uniform
BASE_PRICE = decimal.Decimal('300.00')
PRICE_BALANCE_FACTOR = decimal.Decimal('100') # Divisor for balance contribution to price

# --- Banks to Add ---
CANADIAN_BANKS = [
    "Royal Bank of Canada (RBC)", "Toronto-Dominion Bank (TD)",
    "Bank of Nova Scotia (Scotiabank)", "Bank of Montreal (BMO)",
    "Canadian Imperial Bank of Commerce (CIBC)", "National Bank of Canada",
    "Desjardins Group", "Laurentian Bank of Canada", "HSBC Bank Canada",
    "Canadian Western Bank", "Tangerine Bank", "EQ Bank",
    "Manulife Bank of Canada", "Simplii Financial", "ATB Financial"
]

UK_BANKS = [
    "HSBC Holdings PLC", "Barclays PLC", "Lloyds Banking Group PLC",
    "NatWest Group PLC", "Standard Chartered PLC", "Santander UK PLC",
    "Nationwide Building Society", "TSB Bank PLC", "Metro Bank PLC",
    "Clydesdale Bank PLC", "Virgin Money UK PLC", "Co-operative Bank PLC",
    "Monzo Bank Limited", "Starling Bank Limited", "Revolut Ltd"
]

# Combine banks with their location/country
ALL_BANKS = [(bank, "Canada", "Canada") for bank in CANADIAN_BANKS] + \
            [(bank, "United Kingdom", "UK") for bank in UK_BANKS]

# --- Default Data for New Rows ---
# Category and Info are now dynamic
DEFAULT_ROW_DATA = {
    "Name": "Standard Account",      # Example product name
    "Bin": "",
    "Zip": "",
    "Exp": "",
    "Country": "",  # Will be set based on the bank list
    "Bank": "",     # Will be set from the bank list
    "type": "Checking", # Example type
    "State": "", # Keep blank or assign based on country if needed
    "Gender": "",# Keep blank or randomize? (Using blank for now)
    "DOB": "",   # Keep blank or randomize? (Using blank for now)
    "Status": "1",
    "pdf": "",
    "Location": "" # Will be set based on the bank list
    # Balance and Price are generated dynamically
}

# --- Headers for the new CSV ---
# Ensure all desired columns are present
CSV_HEADERS = [
    "Category", "Name", "Bin", "Zip", "Exp", "Country", "Bank",
    "Balance", "type", "Info", "Price", "State", "Gender",
    "DOB", "Status", "pdf", "Location"
]


# --- Script Logic ---

# Use Decimal context for 2 decimal places
ctx = decimal.Context(prec=20) # Precision should be enough
ctx.rounding = decimal.ROUND_HALF_UP

def quantize_decimal(d):
    """Helper to format Decimal to 2 decimal places."""
    return d.quantize(decimal.Decimal("0.01"), context=ctx)

def create_bank_csv(output_path, banks_with_location, default_data, headers, row_count):
    """
    Creates a new CSV file populated with bank product data,
    including dynamic Category, Info, Balance, and Price.
    """
    generated_rows = []
    num_banks = len(banks_with_location)

    print(f"Generating {row_count} rows for {num_banks} banks...")

    for i in range(row_count):
        # Cycle through banks
        bank_name, country, location = banks_with_location[i % num_banks]

        row = default_data.copy()
        row["Bank"] = bank_name
        row["Country"] = country
        row["Location"] = location

        # --- Dynamic Fields ---
        row["Category"] = bank_name # Category is the bank name
        row["Info"] = "(Online access)+(Account/Routine Number)+(Name And Address)+(Email access)+(Personal Questions)"

        # Generate Balance (10k <= balance < 110k)
        # Convert MIN_BALANCE and MAX_BALANCE to float for uniform, then back to Decimal
        balance_float = random.uniform(float(MIN_BALANCE), float(MAX_BALANCE))
        balance_decimal = ctx.create_decimal(balance_float)
        row["Balance"] = str(quantize_decimal(balance_decimal))

        # Calculate Price (starts at BASE_PRICE + factor of balance)
        price_decimal = BASE_PRICE + (balance_decimal / PRICE_BALANCE_FACTOR)
        row["Price"] = str(quantize_decimal(price_decimal))
        # --- End Dynamic Fields ---


        # --- Optional: Add randomization for other fields here if desired ---
        # Example: Give each product a slightly different name
        # row["Name"] = f"{bank_name} Product Variant {i // num_banks + 1}"
        # --------------------------------------------------------------------

        generated_rows.append(row)

    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=headers)

            # Write header
            writer.writeheader()

            # Write generated rows
            writer.writerows(generated_rows)

        print(f"Successfully created CSV with {len(generated_rows)} rows.")
        print(f"Output written to '{output_path}'.")

    except Exception as e:
        print(f"An error occurred: {e}")

# --- Run the script ---
if __name__ == "__main__":
    # Set higher precision for Decimal calculations globally for the script
    decimal.getcontext().prec = 28
    create_bank_csv(OUTPUT_CSV_PATH, ALL_BANKS, DEFAULT_ROW_DATA, CSV_HEADERS, TARGET_ROW_COUNT)
