import os, json, requests, csv, uuid
from datetime import datetime, timezone
import pandas as pd

print("--- TASKS 3.2-3.7: API INGESTION & LOGGING ---")
os.makedirs('raw/api', exist_ok=True)
os.makedirs('state', exist_ok=True)
os.makedirs('outputs', exist_ok=True)

watermark_file = 'state/api_watermark.json'
log_file = 'outputs/pipeline_run_log.csv'
run_id = str(uuid.uuid4())
start_time = datetime.now(timezone.utc).isoformat()

watermark_before = None
if os.path.exists(watermark_file):
    watermark_before = json.load(open(watermark_file)).get('watermark')

page, has_more, all_records = 1, True, []
error_msg, status = "", "SUCCESS"

try:
    while has_more:
        params = {'page': page, 'per_page': 50}
        if watermark_before: params['updated_after'] = watermark_before
            
        response = requests.get("http://127.0.0.1:8000/api/events", params=params)
        response.raise_for_status() # This triggers the failure block if the server is down
        data = response.json()
        
        records = data['items']
        for r in records:
            r['_ingested_at'] = datetime.now(timezone.utc).isoformat()
            r['_source'] = 'REST API'
            
        all_records.extend(records)
        has_more = data['has_more']
        page = data.get('next_page')

    records_read = len(all_records)
    records_written, duplicates_removed = 0, 0
    watermark_after = watermark_before

    if all_records:
        df = pd.DataFrame(all_records)
        df['updated_at'] = pd.to_datetime(df['updated_at'])
        duplicates_removed = records_read - len(df.drop_duplicates('event_id'))
        df = df.sort_values('updated_at', ascending=False).drop_duplicates('event_id')
        
        df.to_json('raw/api/events.jsonl', orient='records', lines=True)
        records_written = len(df)
        
        watermark_after = df['updated_at'].max().isoformat()
        with open(watermark_file, 'w') as f:
            json.dump({'watermark': watermark_after}, f)
        print("Watermark advanced.")
    else:
        print("No new records to ingest.")

except Exception as e:
    status = "FAILED"
    error_msg = str(e)
    records_read, records_written, duplicates_removed = 0, 0, 0
    watermark_after = watermark_before
    print(f"Pipeline failed safely: {error_msg}")

end_time = datetime.now(timezone.utc).isoformat()

# Append to run log
log_exists = os.path.exists(log_file)
with open(log_file, 'a', newline='') as f:
    writer = csv.writer(f)
    if not log_exists:
        writer.writerow(['run_id', 'start_time', 'end_time', 'status', 'source', 'records_read', 'records_written', 'duplicates_removed', 'watermark_before', 'watermark_after', 'error_message'])
    writer.writerow([run_id, start_time, end_time, status, 'REST API', records_read, records_written, duplicates_removed, watermark_before, watermark_after, error_msg])

print(f"Run logged to {log_file}. Status: {status}")