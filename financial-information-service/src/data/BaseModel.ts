import { Model } from "objection";
import connection from "../utils/knex";

export default class BaseModel extends Model {
  constructor() {
    super();
    Model.knex(connection);
  }
}
