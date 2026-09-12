import requests

print("--- TASK 1.5: REST API PROFILING ---")

# 1. Retrieve page 1
url_page_1 = 'http://127.0.0.1:8000/api/events?page=1&per_page=10'
response_1 = requests.get(url_page_1).json()

# Identify pagination fields
print("Pagination fields found in root JSON:")
print(list(response_1.keys()), "\n")

# Inspect event fields
first_event = response_1['items'][0]
print("Event fields (including nested metadata):")
print(list(first_event.keys()), "\n")
print(f"Sample event_id: {first_event['event_id']}")
print(f"Sample updated_at: {first_event['updated_at']}\n")

# 2. Retrieve page 2 manually
url_page_2 = f"http://127.0.0.1:8000/api/events?page={response_1['next_page']}&per_page=10"
response_2 = requests.get(url_page_2).json()

print(f"Successfully retrieved Page {response_1['next_page']}.")
print(f"Page 2 'has_more' status: {response_2['has_more']}\n")

# 3. Explanation of pagination
print("Why processing only Page 1 is an incomplete ingestion:")
print("The API is paginated, limiting records per request (e.g., 10 per page) to reduce server load. Processing only Page 1 ignores the remaining records indicated by the 'has_more' flag and 'total' count, resulting in massive data loss.")