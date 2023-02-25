# About 💬

The purpose of this repository is to serve as a template or demo for a generic financials application, that allows for visualization of and interaction with bank accounts, cards and payments.

## Structure 🏢

- 🏦 `bank-integration-service` is a Python Flask/AlchemySQL web server that interacts with bank PSD2 APIs. It requires at least registered apps in said banks' sandbox environments. Currently only connected to the Swedish SEB bank.
- 🚢 `infrastructure` contains a Docker based means of spinning up this whole project, including a PostgreSQL database.
- 📃 `financial-information-service` is a NestJS/Prisma back-end, towards which a front-end app would make calls for fetching information. This back-end in turn relies on the `bank-integration-service` for interfacing with the actual bank PSD2 apis. The purpose of this back-end service is only to manage the users of your app and their information.

## Running 🔌

In `infrastructure`:

1. Start only `database` by running `docker-compose up database`.
2. Run the database setup script `./scripts/setup_database.sh`.
3. In a separate terminal window/tab, run `docker-compose up bank-integration-service`, which will populate it's database (`financial`) with the required tables and spin the service up.
4. Run `docker-compose up database financial-information-service`, which will do the same, but for the service that handles users & all features that they have access to.

## TO-DO 👷‍♂️

- In `bank-integration-service`
  - Add logger / error monitoring
  - Add SEB payment initialization.
  - Add error handling - timeouts, connectivity, bad requests
  - Tests with pytest
- In `financial-information-service`
  - Add logger / error monitoring
  - Switch login to use internal user id instead of national identification number (for security purposes).
  - Extend the models to support common fields such as `created_at` upon row insertion and `update_at` upon row updates. E.g -> https://x-team.com/blog/automatic-timestamps-with-postgresql/
  - Rate limiting and customer error messages to avoid software fingerprinting
  - Tests with Jest.

## Roadmap 🛣

- Add a front-end service that displays the financial data of users.
