CREATE TABLE IF NOT EXISTS stocks_data(
    id serial PRIMARY KEY,
    stock_id INTEGER NOT NULL ,
    price FLOAT NOT NULL,
    create_at TIMESTAMP NOT NULL
);
