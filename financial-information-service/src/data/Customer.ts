import BaseModel from "./BaseModel";
import BankAccount from "./BankAccount";
import BankConnection from "./BankConnection";

export default class Customer extends BaseModel {
  id = null;
  nationalIdentificationNumber = null;

  static getTableName() {
    return "customers";
  }

  get bankConnection() {
    return BankConnection.query().where({ customerId: this.id });
  }

  get bankAccounts() {
    return BankAccount.query().where({ customerId: this.id });
  }
}
