## NOTE: Under construction, not functional yet 🚧

# About

The purpose of this repository is to serve as a template or demo for a generic financials application, that allows for visualization and interaction of bank accounts, cards and payments.

## Structure

- `bank-integration-service` is a Python Flask web server that interacts with bank PSD2 apis. It requires at least registered apps in said banks' sandbox environments. Currently only connected to the Swedish SEB bank (and then not fully, only partial auth support exists as of now, but the general structure is in place).
- `docker-setup` contains a Docker based means of spinning up this whole project, including a PostgreSQL database. Also unfinished, as it only supports the `financial-information-service` and database as of the writing of this document.
- `financial-information-service` is a NodeJS/ExpressJS/GraphQL/ObjectionJS back-end, towards which a front-end app would make calls for fetching. This back-end in turn relies on the `bank-integration-service` for interfacing with the actual bank PSD2 apis. The purpose of this back-end service is only to manage the customers of your app and their information.

## TO-DO:

- In `bank-integration-service`
  - Finish the SEB integration - auth, account and card account information fetching.
  - Payment initialization.
  - Work on the file/project structure.
- In `docker-setup`
  - Add the `bank-integration-service` as a container with its own volume.
  - Some volume caching and better secrets management, from, say, .env files instead of fields in the docker-compose YML file would be next too.
- In `financial-information-service`
  - GraphQL resolvers and ORM models need to be completed.
  - Data loaders for more efficient interactions with the db and faster loading times.
  - Database transactions on some critical C(R)UD operations once they're added.
  - Extend the base model to support common fields such as `created_at` upon row insertion and `update_at` upon row updates.
  - The initial Knex migration with tables representing the bank connections, accounts, cards, transactions and customers needs to be written too.
  - Rate limiting on the externally facing endpoints.
  - Some authentication and authorization are necessary as well, to limit who can interact with the API and to make sure customers can only fetch information on their own accounts. That should be based on JWT tokens that contain ACL information (authorization) issued after oAuth2 or BankID (authentication).
  - Tests based on Jest (no testing right now).
