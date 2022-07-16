import BaseModel from "./BaseModel";
import BankConnection from "./BankConnection";
import Customer from "./Customer";
import BankAccountTransaction from "./BankAccountTransaction";

export default class BankAccount extends BaseModel {
  id = "";
  external_id = "";
  customer_id = "";
  bank = "";

  static getTableName() {
    return "bank_accounts";
  }

  async bank_connection() {
    const customer = await Customer.query().findById(this.customer_id);
    const bank_connection = customer
      ? await BankConnection.query().where({
          bank: this.bank,
          customer_national_identification_number:
            customer.national_identification_number,
        })
      : undefined;
    return bank_connection;
  }

  async transactions() {
    return await BankAccountTransaction.query().where({
      bank_account_id: this.id,
    });
  }
}
