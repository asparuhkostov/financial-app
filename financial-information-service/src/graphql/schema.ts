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
    countryOfResidence: SupportedCountry
    nationalIdentificationNumber: String
    """
    bankAccounts: [BankAccount]
    bankConnections: [BankConnection]
    """
  }

  """
  type BankConnection {
    id: ID
    customerNationalIdentificationNumber: String
    bank: SupportedBank
    authToken: String
    refreshToken: String
  }

  type BankAccount {
    id: ID
    externalId: String
    bankConnection: ID
    balance: Float
    transactions: [BankAccountTransaction]
  }

  type BankAccountTransaction {
    id: ID
    bankAccount: ID
  }
  """

  type Query {
    customer(customerId: ID!): Customer
  }
`;
