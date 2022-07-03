import BaseModel from "./BaseModel";

export default class BankAccountTransaction extends BaseModel {
  static getTableName() {
    return "bank_account_transactions";
  }
}
