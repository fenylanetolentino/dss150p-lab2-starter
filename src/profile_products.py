import pandas as pd
import os

parquet_file = 'data/products.parquet'
csv_file = 'data/products_optional_compare.csv'
json_file = 'data/products_optional_compare.json'

print("--- TASK 1.4: products.parquet PROFILING ---")

# 1 & 4. File sizes comparison
pq_size = os.path.getsize(parquet_file)
csv_size = os.path.getsize(csv_file)
json_size = os.path.getsize(json_file)

print(f"Parquet file size: {pq_size} bytes")
print(f"CSV file size:     {csv_size} bytes")
print(f"JSON file size:    {json_size} bytes\n")

# 2. Shape and dtypes
df_pq = pd.read_parquet(parquet_file)
print(f"Shape: {df_pq.shape[0]} rows, {df_pq.shape[1]} columns\n")
print("Columns and Parquet Dtypes:")
print(df_pq.dtypes, "\n")

# 3. Schema behavior comparison
print("Schema Behavior Comparison:")
print("Unlike CSV or JSON (which rely on the reader to infer types from plain text), Parquet embeds a strict, machine-readable schema. It preserves exact data types (like int32, float64, and categoricals) directly within the file metadata.\n")

# 5. Explanation on operational source formats
print("Why Parquet is rarely an operational source format:")
print("Parquet is a columnar format optimized for massive analytical queries and aggregations. Operational (OLTP) systems process continuous row-level transactions (single inserts, updates). Columnar formats are extremely inefficient for row-level writes, so operational systems typically use row-based formats (like JSON/CSV) or relational databases.")