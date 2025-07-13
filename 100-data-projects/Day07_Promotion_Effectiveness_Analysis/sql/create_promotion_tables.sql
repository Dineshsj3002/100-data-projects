-- Orders table (if not already present)
CREATE TABLE IF NOT EXISTS orders (
    order_id TEXT PRIMARY KEY,
    product_id TEXT,
    order_date DATE,
    sales NUMERIC
);

-- Promotions metadata
CREATE TABLE IF NOT EXISTS promotions (
    id SERIAL PRIMARY KEY,
    product_id TEXT,
    promotion_start_date DATE,
    promotion_end_date DATE,
    discount_percent NUMERIC
);
