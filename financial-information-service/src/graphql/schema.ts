import { gql } from "apollo-server-express";

export default gql`
  type Customer {
    id: Int
    nationalIdentificationNumber: String
    bankAccounts: [BankAccount]
    bankConnections: [BankConnection]
  }

  type BankConnection {
    id: ID
    customer: ID
    authToken: String
    refreshToken: String
  }

  type BankAccount {
    id: ID
    balance: Float
    transactions: [BankAccountTransaction]
    bankConnection: ID
  }

  type BankCardAccount extends BankAccount {
    product: String
    usage: String
  }

  type BankAccountTransaction {
    id: ID
    bankAccount: ID
    bookingDate: Date
    invoiced: Boolean
    nameOnCard: String
  }

  type Query {
    customer(customerId: ID!): Customer
  }
`;
