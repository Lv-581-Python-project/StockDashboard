CREATE TABLE IF NOT EXISTS stocks(
    id serial PRIMARY KEY,
    name VARCHAR(16) NOT NULL,
    company_name VARCHAR(128) NOT NULL
);
