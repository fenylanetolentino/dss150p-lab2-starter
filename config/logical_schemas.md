# Logical Schemas for Target Data Warehouse

**1. Customers (from CSV)**
* customer_id: VARCHAR (Primary Key)
* first_name: VARCHAR
* last_name: VARCHAR
* email: VARCHAR (Nullable for now, but needs validation)
* city: VARCHAR
* signup_date: DATE / TIMESTAMP
* customer_segment: VARCHAR

**2. Orders (from JSON)**
* order_id: VARCHAR (Primary Key)
* customer_id: VARCHAR (Foreign Key)
* order_timestamp: TIMESTAMP
* status: VARCHAR
* item_count: INTEGER
* subtotal: FLOAT / DECIMAL
* shipping_fee: FLOAT / DECIMAL
* total_amount: FLOAT / DECIMAL
* shipping: JSONB / VARIANT (Nested object)

**3. Products (from Parquet)**
* product_id: VARCHAR (Primary Key)
* product_name: VARCHAR
* category: VARCHAR
* brand: VARCHAR
* unit_price: FLOAT / DECIMAL
* stock_quantity: INTEGER
* weight_kg: FLOAT / DECIMAL

**4. API Events (from REST API)**
* event_id: VARCHAR (Primary Key)
* customer_id: VARCHAR
* event_type: VARCHAR
* amount: FLOAT / DECIMAL
* updated_at: TIMESTAMP
* metadata: JSONB / VARIANT

**5. Support Tickets (from PostgreSQL)**
* ticket_id: INTEGER (Primary Key)
* customer_id: VARCHAR
* category: VARCHAR
* priority: VARCHAR
* assigned_agent: VARCHAR (Nullable)
* opened_at: TIMESTAMP
* resolved_at: TIMESTAMP (Nullable)
* status: VARCHAR