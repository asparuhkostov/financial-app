import os
import psycopg2

db_connection =  psycopg2.connect(
    host = 'locahost',
    database = "banking",
    user = "postgres",
    password = "postgres"
) if os.environ["ENV"] == "DEV" else psycopg2.connect(
    host =  os.environ["DB_HOST"],
    database = os.environ["DB_DATABASE"],
    user = os.environ["DB_USER"],
    password = os.environ["DB_PASSWORD"]
)