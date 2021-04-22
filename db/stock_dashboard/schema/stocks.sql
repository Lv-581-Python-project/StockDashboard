CREATE TABLE IF NOT EXISTS stocks(
    id serial PRIMARY KEY,
    name VARCHAR(32) NOT NULL,
    company_name VARCHAR(256) NOT NULL,
    country VARCHAR(32) NOT NULL,
    industry VARCHAR(128) NOT NULL,
    sector VARCHAR(32) NOT NULL,
    in_use BOOLEAN NOT NULL DEFAULT FALSE
);
