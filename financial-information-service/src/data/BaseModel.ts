import { Model } from "objection";
import connection from "../utils/knex";

Model.knex(connection);

export default class BaseModel extends Model {
  constructor() {
    super();
  }
}
