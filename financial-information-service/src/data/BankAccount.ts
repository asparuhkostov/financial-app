import BaseModel from "./BaseModel";

export default class BankAccount extends BaseModel {
  static getTableName() {
    return "bank_Accounts";
  }
}
