#!/bin/bash

mkdir data
echo "CREATE DATABASE financial" | psql postgres://postgres:postgres@localhost:5432/postgres