import csv
import random
import uuid
from faker import Faker

# Initialize Faker for generating random values
fake = Faker()

# List of sample data to randomize
bins = ["410039", "520041", "630042"]
levels = ["CLASSIC", "GOLD", "PLATINUM"]
types = ["CREDIT", "DEBIT"]
states = ["CA", "NY", "TX", "FL", "WA"]
banks = ["CITIBANK, N.A.", "CHASE BANK", "WELLS FARGO", "BANK OF AMERICA"]

# Helper function to generate data rows
def generate_row(id):
    base = f"{fake.date_this_year().strftime('%Y_%m_%d')}_US_{fake.bothify('##??').upper()}_{fake.word().upper()}_{fake.phone_number()}"
    return {
        "_id": id,
        "base": base,
        "bin": random.choice(bins),
        "level": random.choice(levels),
        "type": random.choice(types),
        "exp": f"{random.randint(1, 12):02}/{random.randint(23, 30)}",
        "expmonth": None,
        "expyear": None,
        "city": fake.city(),
        "state": random.choice(states),
        "country": "US",
        "zip": fake.zipcode(),
        "bank": random.choice(banks),
        "refundable": random.randint(0, 1),
    }

# Generate 200 rows of data
data = [generate_row(i) for i in range(1, 201)]

# Save to CSV
output_file = "random_data.csv"
with open(output_file, mode="w", newline="") as csvfile:
    fieldnames = data[0].keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)

print(f"Random data saved to {output_file}")
