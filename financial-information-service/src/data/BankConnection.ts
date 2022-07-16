import BaseModel from "./BaseModel";

export default class BankConnection extends BaseModel {
  id = "";
  customer_national_identification_number = "";
  bank = "";
  auth_token = "";
  refresh_token = "";

  static getTableName() {
    return "bank_connections";
  }
}
