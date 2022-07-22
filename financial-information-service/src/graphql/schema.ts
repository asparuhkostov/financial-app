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

  enum SupportedCurrency {
    SEK
    DKK
    NOK
    EUR
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
    bank_connection_id: ID
    name: String
    currency: SupportedCurrency
    iban: String
    bank: String
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
