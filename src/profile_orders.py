import json
import pandas as pd

file_path = 'data/orders.json'
print("--- TASK 1.3: orders.json PROFILING ---")

# Load raw JSON
with open(file_path, 'r') as f:
    raw_data = json.load(f)

# 1. Confirm root structure and count
print(f"Is root structure a list of records? {isinstance(raw_data, list)}")
print(f"Total records: {len(raw_data)}\n")

# 2. List keys and nested fields
first_record = raw_data[0]
print(f"Top-level keys: {list(first_record.keys())}")
nested_fields = [k for k, v in first_record.items() if isinstance(v, dict)]
print(f"Nested field(s) identified: {nested_fields}\n")

# 3. Load into pandas to inspect types and missing keys
df = pd.json_normalize(raw_data)
print("Columns and Inferred Types (Identifying Timestamps & Numerics):")
print(df.dtypes, "\n")

print("Missing Values by Column (Missing Keys):")
print(df.isnull().sum(), "\n")

# 4. Downstream representation of nested objects
print("Two ways to represent the nested 'shipping' object downstream:")
print("1. Flatten the object into separate columns (e.g., shipping_method, shipping_cost).")
print("2. Store it as a native JSON/Struct data type (e.g., JSONB in PostgreSQL or VARIANT in Snowflake).")