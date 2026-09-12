import os
import hashlib
import shutil
from datetime import datetime, timezone
import json

print("--- TASK 3.1: RAW FILE INGESTION ---")
os.makedirs('raw/files', exist_ok=True)
os.makedirs('state', exist_ok=True)

files = ['data/customers.csv', 'data/orders.json', 'data/products.parquet']
manifest_path = 'state/file_manifest.json'
manifest = json.load(open(manifest_path)) if os.path.exists(manifest_path) else {}

def get_sha256(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

for file_path in files:
    filename = os.path.basename(file_path)
    file_hash = get_sha256(file_path)
    
    if filename in manifest and manifest[filename]['sha256'] == file_hash:
        print(f"Skipping {filename}: Hash {file_hash} already ingested.")
        continue
        
    shutil.copy2(file_path, f"raw/files/{filename}")
    manifest[filename] = {
        "file_name": filename,
        "ingested_at": datetime.now(timezone.utc).isoformat(),
        "byte_size": os.path.getsize(file_path),
        "sha256": file_hash
    }
    print(f"Ingested {filename}")

with open(manifest_path, 'w') as f:
    json.dump(manifest, f, indent=2)