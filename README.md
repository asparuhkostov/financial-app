## NOTE: Under construction, not functional yet 🚧

# About 💬

The purpose of this repository is to serve as a template or demo for a generic financials application, that allows for visualization of and interaction with bank accounts, cards and payments.

## Structure 🏢

- `bank-integration-service` is a Python Flask/AlchemySQL web server that interacts with bank PSD2 APIs. It requires at least registered apps in said banks' sandbox environments. Currently only connected to the Swedish SEB bank.
- `infrastructure` contains a Docker based means of spinning up this whole project, including a PostgreSQL database.
- `financial-information-service` is a NodeJS/ExpressJS/GraphQL/ObjectionJS back-end, towards which a front-end app would make calls for fetching information. This back-end in turn relies on the `bank-integration-service` for interfacing with the actual bank PSD2 apis. The purpose of this back-end service is only to manage the customers of your app and their information.

## TO-DO 👷‍♂️:

- In `bank-integration-service`
  - Add SEB account information fetching.
  - Add SEB payment initialization.
- In `infrastructure`
  - Some volume caching and better secrets management, from, say, .env files instead of fields in the docker-compose YML file would be next too.
  - Fixes on the `bank-integration-service container` are required, right now I run said service outside the Docker env with `python app.py` after exporting the env variables in my terminal session.
- In `financial-information-service`
  - GraphQL resolvers and ORM models need to be completed.
  - Data loaders for more efficient interactions with the db and faster loading times.
  - Database transactions on some critical C(R)UD operations once they're added.
  - Extend the base model to support common fields such as `created_at` upon row insertion and `update_at` upon row updates.
  - The initial Knex migration with tables representing the bank connections, accounts, cards, transactions and customers needs to be written too.
  - Rate limiting on the externally facing endpoints.
  - Some authentication and authorization are necessary as well, to limit who can interact with the API and to make sure customers can only fetch information on their own accounts. That should be based on JWT tokens that contain ACL information (authorization) issued after oAuth2 or BankID (authentication).
  - Tests based on Jest (no testing right now).
- Overall
  - Move the bank transactions table into either its own PostgreSQL instance or leave the entries unstructured and move it into a Cassandra database (which would also require some changes in how said transactions are served by the `financial-information-service`).

## Running:

In `infrastructure`:

1. Start only `database` by running `docker-compose up database`,
2. then run the database setup script in the `scripts` folder by `./scripts/setup_database.sh`.
3. In a separate terminal window/tab, run `docker-compose up financial-information-service`, so that the knex migrations in said service would populate the database with the required tables.
4. All done! You can run `docker-compose up database financial-information-service bank-integration-service` to have the whole environment up.
