import os
import sys
import requests
from uuid import uuid4


integrations_dir = os.getcwd() + "/integrations"
sys.path.append(integrations_dir)
models_dir = os.getcwd() + "/models"
sys.path.append(models_dir)


from integrations.template import TemplateProvider
from models.BankConnections import BankConnections
from models.BankAccounts import BankAccounts
from models.BankAccountTransactions import BankAccountTransactions


SEB_CLIENT_ID = os.environ["SEB_CLIENT_ID"]
SEB_CLIENT_SECRET = os.environ["SEB_CLIENT_SECRET"]


API_BASE_URL = 'https://api-sandbox.sebgroup.com'
API_AUTH_ENDPOINT = 'auth/v3/authorizations'
API_TOKEN_ENDPOINT = 'auth/v3/tokens'
API_ACCOUNTS_ENDPOINT = 'ais/v7/identified2/accounts'
API_TRANSACTIONS_ENDPOINT = "transactions"


def create_authorization_request():
    url = f"{API_BASE_URL}/{API_AUTH_ENDPOINT}"
    data = {
        "client_id": SEB_CLIENT_ID,
        "scope": "psd2_accounts psd2_payments",
        "start_mode": "ast"
    }
    r = requests.post(url, json=data)
    d = r.json()
    return d["auth_req_id"]


def get_bankid_autostart_token(auth_req_id):
    r = requests.get(f"{API_BASE_URL}/{API_AUTH_ENDPOINT}/{auth_req_id}")
    d = r.json()
    return d["autostart_token"]


def get_token_data(auth_req_id):
    data = {
    "client_id": SEB_CLIENT_ID,
    "client_secret": SEB_CLIENT_SECRET,
    "auth_req_id": auth_req_id,
    }
    res = requests.post(f"{API_BASE_URL}/{API_TOKEN_ENDPOINT}", json=data)
    return res.json()


class SEB(TemplateProvider):
    def init_auth(self):
        auth_req_id = create_authorization_request()
        return {
            "auth_request_id": auth_req_id,
            "bank_id_autostart_token": get_bankid_autostart_token(auth_req_id)
        }

  
    def verify_login(self, auth_req_id):
        res = requests.get(f"{API_BASE_URL}/{API_AUTH_ENDPOINT}/{auth_req_id}")
        return {"is_complete": True if res.json()["status"] == "COMPLETE" else False}


    def create_bank_connection(self, auth_req_id):
        token_data = get_token_data(auth_req_id)
        bank_connection = BankConnections(
            id = uuid4(), 
            bank="seb",
            customer_national_identification_number = self.customer_national_identification_number,
            access_token=token_data["access_token"], 
            refresh_token=token_data["refresh_token"],
        )
        self.db.session.add(bank_connection)
        self.db.session.commit()
        return bank_connection.serialize()


    def refresh_bank_connection(self):
        bank_connection = BankConnections.query.filter_by(customer_national_identification_number=self.customer_national_identification_number).first()
        data = {
            "client_id": SEB_CLIENT_ID,
            "client_secret": SEB_CLIENT_SECRET,
            "refresh_token": bank_connection.refresh_token,
        }
        res = requests.post(f"{API_BASE_URL}/{API_TOKEN_ENDPOINT}", json=data)

        token_data = res.json()
        BankConnections.access_token = token_data["access_token"]
        BankConnections.refresh_token = token_data["refresh_token"]
        self.db.session.commit()

        return bank_connection.serialize()


    def get_bank_accounts(self):
        bank_connection = BankConnections.query.filter_by(customer_national_identification_number=self.customer_national_identification_number).first()
        headers = {
            "Authorization": f"Bearer {bank_connection.access_token}",
            "X-Request-ID": str(uuid4()),
            "Accept": "application/json",
        }
        res = requests.get(f"{API_BASE_URL}/{API_ACCOUNTS_ENDPOINT}", headers=headers)

        accounts_data = res.json()
        inserted_accounts = []
        for i in accounts_data["accounts"]:
            account = BankAccounts(
                id = uuid4(),
                external_id = res["accounts"][i].resourceId,
                bank="seb",
                bank_connection_id = bank_connection.id,
                name = res["accounts"][i].name,
                currency = res["accounts"][i].currency,
                iban = res["accounts"][i].iban
            )
            self.db.session.add(account)
            self.db.session.commit()
            inserted_accounts.append(account.serialize())

        return inserted_accounts


    def get_bank_account_transactions(self, bank_account_external_id):
        bank_connection = BankConnections.query.filter_by(customer_national_identification_number=self.customer_national_identification_number).first()
        headers = {
            "Authorization": f"Bearer {bank_connection.access_token}",
            "X-Request-ID": str(uuid4()),
            "Accept": "application/json",
        }
        res = requests.get(f"{API_BASE_URL}/{API_ACCOUNTS_ENDPOINT}/{bank_account_external_id}/{API_TRANSACTIONS_ENDPOINT}", headers=headers)

        transactions_data = res.json()
        inserted_transactions = []
        for t in transactions_data["transactions"]:
            transaction = BankAccountTransactions(
                id = uuid4(),
                external_id = res["transactions"][t].resourceId,
                bank_account_id = bank_account_external_id
            )
            self.db.session.add(transaction)
            self.db.session.commit()
            inserted_transactions.append(transaction.serialize())

        return inserted_transactions
