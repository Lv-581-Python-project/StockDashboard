\set scripts_root `echo $SQL_SCRIPTS_ROOT`
\i :scripts_root/schema/dashboard.sql
\i :scripts_root/schema/dashboard_has_stocks.sql
\i :scripts_root/schema/stocks.sql
\i :scripts_root/schema/stocks_data.sql
