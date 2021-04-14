# Stock Dashboard [![Coverage Status](https://coveralls.io/repos/github/Lv-581-Python-project/StockDashboard/badge.svg?branch=develop)](https://coveralls.io/github/Lv-581-Python-project/StockDashboard?branch=develop)


### Docker-compose setup
1. Create `.env` file (skip if exists)
2. Fill `.env` file according to this template
   ```
   POSTGRES_USER=your_username
   
   POSTGRES_PASSWORD=your_password
   
   POSTGRES_DB=your_db_name
   
   RABBITMQ_ERLANG_COOKIE=your_rabbitmq_erland_cookie_secret_key
   ```
3. Run `docker-compose up`

- In case of editing some of this params you will likely have to remove `pg_data/` or `rmq-data/`

### Database Init

To create and to fill database go to
folder data/StockDashboard and type command to run script:
```bash
 psql -U <username> -d <dbname> -a -f <script_name>
```
- To create run `CREATE_DB.sql`
- To fill run `INSERT_DATA.sql`

### Environment variables

Insert to `.env`:
```
   export FLASK_APP=your_path_to_app
   export FLASK_SECRET_KEY=your_flask_secret_key
   export APPLICATION_HOST=your_application_host_address
   export PROD_ROOT=your_full_path_to_app
   
   export MINCONN=min_database_pool_connections
   export MAXCONN=max_database_pool_connections
   export POSTGRES_USER=your_postgres_user
   export POSTGRES_PASSWORD=your_postgres_password
   export POSTGRES_DB=your_postgres_database_name
   export POSTGRES_PORT=your_postgres_post
   export POSTGRES_HOST=your_postgres_host
   
   export LOGGING_CONF=your_path_to_pool_logging_file  # (logging.conf)
   
   export RABBITMQ_ERLANG_COOKIE=your_rmq_erl_cookie
   export RABBITMQ_CONNECTION_HOST=your_rmq_host
   export RABBITMQ_DELIVERY_MODE=your_rmq_delivery_mode  # default is 2 (PERSISTENT)
   
   export MAIL_PORT=your_smtp_email_port
   export MAIL_HOST=your_smtp_email_host
   export MAIL_USE_TLS=your_tls_config_value
   export MAIL_USERNAME=your_email_username
   export MAIL_PASSWORD=your_email_password
```
