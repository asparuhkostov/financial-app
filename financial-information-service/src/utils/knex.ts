import knex from "knex";

const env: string = process.env.NODE_ENV || "development";
const knexConfiguration: { [key: string]: any } = require("../../knexfile");
const connection = knex(knexConfiguration[env]);
export default connection;
