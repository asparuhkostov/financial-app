#!/bin/bash

echo "CREATE DATABASE financial" | psql postgres://postgres:postgres@localhost:5432/postgres
echo "CREATE DATABASE main" | psql postgres://postgres:postgres@localhost:5432/postgres

echo "CREATE TABLE bank_connections ( id varchar primary key, bank varchar not null, customer_national_identification_number varchar not null, access_token varchar not null, refresh_token varchar not null);" | psql postgres://postgres:postgres@localhost:5432/financial
