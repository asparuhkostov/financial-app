import BaseModel from "./BaseModel";

export default class Customer extends BaseModel {
  static getTableName() {
    return "customers";
  }
}
