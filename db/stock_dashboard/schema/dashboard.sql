CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS dashboard(
    id serial PRIMARY KEY,
    dashboard_uuid uuid DEFAULT uuid_generate_v4 ()
);
