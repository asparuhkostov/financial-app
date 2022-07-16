import BaseModel from "./BaseModel";
import BankAccount from "./BankAccount";
export default class Customer extends BaseModel {
  id = null;
  national_identification_number = "";
  country_of_residence = "";

  static getTableName() {
    return "customers";
  }

  bank_accounts() {
    return BankAccount.query().where({ customer_id: this.id });
  }
}
