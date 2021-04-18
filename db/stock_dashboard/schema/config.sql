CREATE TABLE IF NOT EXISTS config(
    id serial PRIMARY KEY,
    config_hash VARCHAR(8) UNIQUE NOT NULL
);
