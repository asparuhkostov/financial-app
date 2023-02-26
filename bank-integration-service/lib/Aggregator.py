from models.BankConnections import BankConnections
from models.BankAccounts import BankAccounts
from models.BankAccountTransactions import BankAccountTransactions
import os
import sys


models_dir = os.getcwd() + "/models"
sys.path.append(models_dir)


# Collects and formats all financial information
# on a user.
class Aggregator:
    def __init__(self, national_identification_number):
        self.national_identification_number = national_identification_number

    def compile_financial_information():
        financial_information = {}

        connections = BankConnections.query.filter_by(
            national_identification_number=self.national_identification_number
        )

        for c in connections:
            accounts = BankAccounts.query.filter_by(bank_connection_id=c.id)
            for a in accounts:
                transactions = BankAccountTransactions.query.filter_by(
                    bank_account_id=a.id)
                serialised_transactions = []
                for t in transactions:
                    serialised_transactions.append(t.serialize())

                account_data = {
                    account: a.serialize(),
                    transactions: serialised_transactions
                }
                if a.bank in financial_information:
                    financial_information[a.bank].append(account_data)
                else:
                    financial_information[a.bank] = [
                        account_data
                    ]
        return financial_information
