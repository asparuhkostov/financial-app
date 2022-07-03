import BaseModel from "./BaseModel";

export default class BankConnection extends BaseModel {
  static getTableName() {
    return "bank_connections";
  }
}
