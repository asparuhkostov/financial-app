# About 💬

The purpose of this repository is to serve as a template or demo for a generic financials application, that allows for visualization of and interaction with bank accounts, cards and payments.

## Structure 🏢

- 🏦 `bank-integration-service` is a Python Flask/AlchemySQL web server that interacts with bank PSD2 APIs. It requires at least registered apps in said banks' sandbox environments. Currently only connected to the Swedish SEB bank.
- 🚢 `infrastructure` contains a Docker based means of spinning up this whole project, including a PostgreSQL database.
- 📃 `financial-information-service` is a NodeJS/ExpressJS/GraphQL/ObjectionJS back-end, towards which a front-end app would make calls for fetching information. This back-end in turn relies on the `bank-integration-service` for interfacing with the actual bank PSD2 apis. The purpose of this back-end service is only to manage the customers of your app and their information.

## Running 🔌

In `infrastructure`:

1. Start only `database` by running `docker-compose up database`,
2. then run the database setup script `./scripts/setup_database.sh`.
3. In a separate terminal window/tab, run `docker-compose up financial-information-service`, so that the knex migrations in said service would populate the database with the required tables.
4. All done! You can run `docker-compose up database financial-information-service bank-integration-service` to have the whole environment up.

## TO-DO 👷‍♂️

- In `bank-integration-service`
  - Add SEB payment initialization.
  - Add error handling to PSD2 integration components
- In `financial-information-service`
  - Data loaders for more efficient interactions with the db and faster loading times. E.g using this -> https://github.com/graphql/dataloader
  - Extend the base model to support common fields such as `created_at` upon row insertion and `update_at` upon row updates. E.g -> https://x-team.com/blog/automatic-timestamps-with-postgresql/
  - Rate limiting and customer error messages to avoid software fingerprinting
  - Authentication and authorization for the GraphQL queries -> https://blog.logrocket.com/authorization-access-control-graphql/
  - Unit tests with Jest.

## Roadmap 🛣

- Introduce Cassandra for storing the bank account transactions.
