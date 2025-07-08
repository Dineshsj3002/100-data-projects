CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    product_name TEXT,
    product_category TEXT,
    order_quantity INT,
    subtotal NUMERIC,
    discount_percent NUMERIC,
    total NUMERIC,
    city TEXT,
    state TEXT,
    order_date DATE
);
