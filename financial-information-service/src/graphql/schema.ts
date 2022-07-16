import { gql } from "apollo-server-express";

export default gql`
  enum SupportedBank {
    SEB
  }

  enum SupportedCountry {
    SE
    DK
    NO
    FI
  }

  type Customer {
    id: ID
    country_of_residence: SupportedCountry
    national_identification_number: String
    bank_accounts: [BankAccount]
    bank_connections: [BankConnection]
  }

  type BankConnection {
    id: ID
    customer_national_identification_number: String
    bank: SupportedBank
    auth_token: String
    refresh_token: String
  }

  type BankAccount {
    id: ID
    external_id: String
    customer_id: ID
    bank_connection: ID
    transactions: [BankAccountTransaction]
  }

  type BankAccountTransaction {
    id: ID
    bank_account: ID
  }

  type Query {
    customer(customerId: ID!): Customer
  }
`;
