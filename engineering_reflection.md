# Engineering Reflection

1. **Why should source profiling occur before implementation?** 
Profiling reveals data quality issues, schemas, and structural anomalies (like nested JSON) so ingestion logic and contracts are designed accurately rather than failing blindly in production.

2. **Event time vs Ingestion time:** 
Event time (`updated_at`) is when the action occurred in the source system. Ingestion time (`_ingested_at`) is the exact metadata timestamp when the pipeline processed and stored the record.

3. **Why is event_id insufficient for duplicates?** 
The API intentionally repeats `event_id` values for state changes. Using only the ID risks retaining outdated states; deduplication must explicitly keep the record with the greatest `updated_at`.

4. **Why watermark advance only after success?** 
If advanced before a durable write, a subsequent pipeline crash would cause the next run to skip those records, resulting in permanent data loss.

5. **Limitation of updated_after > watermark:** 
If multiple source records share the exact same timestamp, a strictly "greater than" query will permanently skip concurrent records that had not yet been returned by the API.

6. **Duplicate prevention vs Idempotency:** 
Duplicate prevention resolves bad or updated source data (duplicated IDs). Idempotency guarantees the pipeline itself will not multiply records in the raw area if executed multiple times.

7. **Why preserve source values in raw?** 
Preserving an exact replica ensures an auditable historical record. If downstream business logic changes, data can be reprocessed without querying the source system again.

8. **OLTP degradation:** 
Unbounded analytical queries consume heavy CPU and memory, which can lock tables or crash the live application serving real customers.

9. **API rate limit mitigation:** 
Introduce a `time.sleep()` delay inside the pagination loop to throttle outgoing requests, or implement exponential backoff retries on 429 status codes.

10. **PostgreSQL pipeline extension:** 
Track the `max(updated_at)` or `max(ticket_id)` as the watermark state and query incrementally. Write to the raw area using an atomic `UPSERT` strategy to maintain idempotency.


AI Use Disclosure: I utilized a generative AI assistant (Gemini) as a debugging and formatting thought partner during this lab. Specifically, AI was used to help troubleshoot Docker container connection errors, correct Git tracking commands and format the structural layout of my final markdown and text documents. I actively executed, reviewed, and validated all terminal commands, SQL queries, and pipeline runs to ensure I understood the underlying logic before submitting.