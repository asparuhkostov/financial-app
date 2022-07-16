/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
exports.up = function (knex) {
  return Promise.all([
    knex.schema.createTable("customers", (table) => {
      table.uuid("id").primary();
      table.string("national_identification_number").notNullable();
      table.string("country_of_residence").notNullable();
    }),
    knex.schema.createTable("bank_connections", (table) => {
      table.uuid("id").primary();
      table.string("bank").notNullable();
      table.string("customer_national_identification_number").notNullable();
      table.string("access_token").notNullable();
      table.string("refresh_token").notNullable();
    }),
    knex.schema.createTable("bank_accounts", (table) => {
      table.uuid("id").primary();
      table.string("external_id").notNullable();
      table.string("bank").notNullable();
      table.uuid("customer_id").references("customers.id");
    }),
    knex.schema.createTable("bank_account_transactions", (table) => {
      table.uuid("id").primary();
      table.uuid("bank_account_id").references("bank_accounts.id");
    }),
  ]);
};

/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
exports.down = async function (knex) {
  return Promise.all(
    [
      "customers",
      "bank_connections",
      "bank_accounts",
      "bank_account_transactions",
    ].map((t) => knex.schema.dropTableIfExists(t))
  );
};
