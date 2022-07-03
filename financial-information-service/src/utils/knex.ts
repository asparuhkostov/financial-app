import knex from "knex";

const knexConfiguration = require("../../knexfile");
const connection = knex(knexConfiguration);
export default connection;
