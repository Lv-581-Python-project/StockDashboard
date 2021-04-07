# Stock Dashboard

### Add the secret key
```
Create .env file in ~StockDashboard/stock_dashboard_api with 
export FLASK_SECRET_KEY = 'Your Secret Key'
```

### Docker-compose setup
1. Create `.env` file (skip if exists)
2. Fill `.env` file according to this template
   ```
   export FLASK_APP=path_to_app
   export FLASK_SECRET_KEY=flask_secret_k
   export APPLICATION_HOST='http://127.0.0.1:5000/'
   export PROD_ROOT='/home/slavko/Work/StockDashboard/stock_dashboard_api'
   
   export MINCONN=1
   export MAXCONN=20
   export POSTGRES_USER='postgres'
   export POSTGRES_PASSWORD='postgres'
   export POSTGRES_DB='stock_dashboard'
   export POSTGRES_PORT=5432
   export POSTGRES_HOST='localhost'
   
   export LOGGING_CONF='/home/slavko/Work/StockDashboard/stock_dashboard_api/logging.conf'
   
   export RABBITMQ_ERLANG_COOKIE="set-cookie"
   export RABBITMQ_CONNECTION_HOST="localhost"
   export RABBITMQ_DELIVERY_MODE=2
   
   export MAIL_PORT=587
   export MAIL_HOST='smtp.googlemail.com'
   export MAIL_USE_TLS=1
   export MAIL_USERNAME='stockdashboard581@gmail.com'
   export MAIL_PASSWORD='stockdashboard'
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
