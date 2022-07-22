import { Knex } from "knex";

export async function up(knex: Knex): Promise<void> {
  knex.schema.alterTable("bank_account_transactions", (t) => {
    t.string("external_id");
  });
}

export async function down(knex: Knex): Promise<void> {
  knex.schema.alterTable("bank_account_transactions", (t) => {
    t.dropColumn("external_id");
  });
}
