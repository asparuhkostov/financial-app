/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
exports.up = function (knex) {
  knex.schema.createTable("customers", (table) => {
    table.uuid("id").primary();
    table.string("national_identification_number");
    table.string("country_of_residence");
  });
  knex.schema.createTable("bank_connections", (table) => {
    table.uuid("id").primary();
    table.foreign("customer").references("customers.id");
    table.string("bank");
    table.string("auth_token");
    table.string("refresh_token");
  });
  knex.schema.createTable("bank_accounts", (table) => {
    table.uuid("id").primary();
    table.string("external_id");
    table.foreign("bank_connections").references("bank_connections.id");
  });
};

/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
exports.down = function (knex) {
  ["customers", "bank_connections", "bank_accounts"].forEach((t) =>
    knex.schema.dropTableIfExists(t)
  );
};
