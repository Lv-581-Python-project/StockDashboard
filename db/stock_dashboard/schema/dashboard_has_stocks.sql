CREATE TABLE IF NOT EXISTS dashboard_has_stocks(
    stock_id INTEGER NOT NULL ,
    dashboard_uuid uuid NOT NULL,
    datetime_from TIMESTAMP NOT NULL,
    datetime_to TIMESTAMP NOT NULL
);
