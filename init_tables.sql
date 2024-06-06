CREATE TABLE IF NOT EXISTS sites (
    id int PRIMARY KEY,
    name VARCHAR(255),
    api_link TEXT,
    num_items_on_discount INT
);

CREATE TABLE IF NOT EXISTS extractions (
    id UUID PRIMARY KEY,
    num_extracted INT,
    num_imported INT,
    extraction_start_time TIMESTAMP,
    extraction_end_time TIMESTAMP,
    import_start_time TIMESTAMP,
    import_end_time TIMESTAMP
);

CREATE TABLE IF NOT EXISTS items (
    id UUID PRIMARY KEY,
    id_from_site VARCHAR(255),
    name VARCHAR(255),
    link TEXT,
    base_price FLOAT,
    promo_price FLOAT,
    gender VARCHAR(255),
    colors TEXT[],
    sizes TEXT[],
    rating FLOAT,
    num_ratings INT,
    sale_start DATE,
    discount_status VARCHAR(255),
    site_id INT REFERENCES sites (id),
    extraction_id UUID REFERENCES extractions (id),
    image_links TEXT[]
);

CREATE TABLE IF NOT EXISTS item_change_records (
    id UUID PRIMARY KEY,
    item_id UUID REFERENCES items (id),
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    field_changed VARCHAR(255),
    from_value TEXT,
    to_value TEXT
);
