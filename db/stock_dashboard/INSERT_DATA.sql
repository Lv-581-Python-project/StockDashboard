\set scripts_root `echo $SQL_SCRIPTS_ROOT`
\i :scripts_root/data/dashboard.sql
\i :scripts_root/data/dashboard_has_stocks.sql
\i :scripts_root/data/stocks.sql
-- \i data/stocks_data.sql
