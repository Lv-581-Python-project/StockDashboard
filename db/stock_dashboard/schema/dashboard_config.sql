CREATE TABLE IF NOT EXISTS dashboard_config(
    id serial PRIMARY KEY,
    config_hash VARCHAR(8) UNIQUE NOT NULL
);
