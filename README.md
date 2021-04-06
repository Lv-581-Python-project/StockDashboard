Stock Dashboard
### Docker-compose setup
1. Create .env file (skip if exists)
2. Fill .env file according to this template
   
   `POSTGRES_USER=your_username`
   
   `POSTGRES_PASSWORD=your_password`
   
   `POSTGRES_DB=your_db_name`
   
   `RABBITMQ_ERLANG_COOKIE=your_rabbitmq_erland_cookie_secret_key`
3. Run `docker-compose up`

- In case of editing some of this params you will likely have to remove `pg_data/` or `rmq-data/`

### Date Base Init

To create and to fill date base go to
folder data/StockDashboard and type command to run script:
```bash
 psql -U <username> -d <dbname> -a -f <script_name>
```
- To create run CREATE_DB.sql
- To fill run INSERT_DATA.sql