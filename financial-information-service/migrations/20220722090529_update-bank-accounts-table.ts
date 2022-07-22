import { Knex } from "knex";

export async function up(knex: Knex): Promise<void> {
  knex.schema.alterTable("bank_accounts", (t) => {
    t.dropColumn("customer_id");
    t.uuid("bank_connection_id").references("bank_connections.id");
    t.string("name");
    t.string("currency");
    t.string("iban");
  });
}

export async function down(knex: Knex): Promise<void> {
  knex.schema.alterTable("bank_accounts", (t) => {
    t.uuid("customer_id").references("customers.id");
    t.dropColumn("bank_connection_id");
    t.dropColumn("name");
    t.dropColumn("currency");
    t.dropColumn("iban");
  });
}
