f = open("/home/lurakil/StockDashboard/db/stock_dashboard/data/stock_data.txt")
g = open("/home/lurakil/StockDashboard/db/stock_dashboard/data/stocks_data.sql", 'a')
for line in f:
    g.write(line)
f.close()
