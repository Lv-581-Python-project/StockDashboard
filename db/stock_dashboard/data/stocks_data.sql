COPY stocks_data(stock_id, price, created_at)
FROM '/home/steven/github/StockDashboard/db/stock_dashboard/data/data.csv'
DELIMITER ',';
