import pandas as pd
import os

file_path = 'data/customers.csv'
print("--- TASK 1.2: customers.csv PROFILING ---")

# 1. File size and counts
size_bytes = os.path.getsize(file_path)
print(f"File size: {size_bytes} bytes")
df = pd.read_csv(file_path)
print(f"Shape: {df.shape[0]} rows, {df.shape[1]} columns\n")

# 2. Columns and Inferred Types
print("Columns and Inferred Types:")
print(df.dtypes, "\n")

# 3. Missing values
print("Missing Values by Column:")
print(df.isnull().sum(), "\n")

# 4. Exact duplicate rows
print(f"Exact duplicate rows: {df.duplicated().sum()}\n")

# 5. Test customer_id uniqueness
id_duplicates = df.duplicated(subset=['customer_id']).sum()
print(f"Duplicate customer_id values: {id_duplicates}")
print(f"Is customer_id strictly unique? {id_duplicates == 0}\n")

# 6. Candidate validation rules
print("Candidate Validation Rules:")
print("1. customer_id must not be null and must be unique.")
print("2. email must be a valid email format.")
print("3. signup_date must be a valid datetime.")