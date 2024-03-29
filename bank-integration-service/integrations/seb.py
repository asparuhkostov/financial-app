from models.BankAccountTransactions import BankAccountTransactions
from models.BankAccounts import BankAccounts
from models.BankConnections import BankConnections
from integrations.template import TemplateProvider


import os
import sys
import requests
from uuid import uuid4
import datetime
import json


integrations_dir = os.getcwd() + "/integrations"
sys.path.append(integrations_dir)
models_dir = os.getcwd() + "/models"
sys.path.append(models_dir)


SEB_CLIENT_ID = os.environ["SEB_CLIENT_ID"]
SEB_CLIENT_SECRET = os.environ["SEB_CLIENT_SECRET"]


API_BASE_URL = 'https://api-sandbox.sebgroup.com'
API_AUTH_ENDPOINT = 'auth/v3/authorizations'
API_TOKEN_ENDPOINT = 'auth/v3/tokens'
API_ACCOUNTS_ENDPOINT = 'ais/v8/identified2/accounts'
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
    res = requests.post(
        f"{API_BASE_URL}/{API_TOKEN_ENDPOINT}",
        json=data
    )
    return res.json()


class SEB(TemplateProvider):
    def __init__(self, db):
        self.db = db

    # https://developer.sebgroup.com/products/authorization/decoupled-authorization
    def init_auth(self):
        auth_req_id = create_authorization_request()
        return {
            "auth_request_id": auth_req_id,
            "bank_id_autostart_token": get_bankid_autostart_token(auth_req_id)
        }

    def verify_login(self, auth_req_id):
        res = requests.get(f"{API_BASE_URL}/{API_AUTH_ENDPOINT}/{auth_req_id}")
        is_complete = True if res.json()["status"] == "COMPLETE" else False

        return {"is_complete": is_complete}

    def create_bank_connection(self, auth_req_id, national_identification_number):
        token_data = get_token_data(auth_req_id)
        new_connection_id = str(uuid4())
        now = datetime.datetime.now()
        bank_connection = BankConnections(
            id=new_connection_id,
            bank="seb",
            national_identification_number=national_identification_number,
            access_token=token_data["access_token"],
            refresh_token=token_data["refresh_token"],
            created_at=now,
            updated_at=now
        )
        self.db.session.add(bank_connection)
        self.db.session.commit()
        return bank_connection.serialize()

    def refresh_bank_connection(self, national_identification_number):
        bank_connection = BankConnections.query.filter_by(
            national_identification_number=national_identification_number
        ).first()
        data = {
            "client_id": SEB_CLIENT_ID,
            "client_secret": SEB_CLIENT_SECRET,
            "refresh_token": bank_connection.refresh_token,
        }
        res = requests.post(
            f"{API_BASE_URL}/{API_TOKEN_ENDPOINT}",
            json=data
        )

        token_data = res.json()
        bank_connection.access_token = token_data["access_token"]
        bank_connection.refresh_token = token_data["refresh_token"]
        bank_connection.updated_at = datetime.datetime.now()
        self.db.session.commit()

        return bank_connection.serialize()

    def get_bank_accounts(self, national_identification_number):
        bank_connection = BankConnections.query.filter_by(
            national_identification_number=national_identification_number
        ).first()

        headers = {
            "Authorization": f"Bearer {bank_connection.access_token}",
            "X-Request-ID": str(uuid4()),
            "Accept": "application/json",
        }
        res = requests.get(
            f"{API_BASE_URL}/{API_ACCOUNTS_ENDPOINT}",
            headers=headers
        )
        accounts_data = res.json()

        inserted_accounts = []
        for i in accounts_data["accounts"]:
            now = datetime.datetime.now()
            account = BankAccounts(
                id=str(uuid4()),
                external_id=i["resourceId"],
                bank="seb",
                bank_connection_id=bank_connection.id,
                name=i["name"],
                currency=i["currency"],
                iban=i["iban"],
                created_at=now,
                updated_at=now
            )
            self.db.session.add(account)
            self.db.session.commit()
            inserted_accounts.append(account.serialize())

        return inserted_accounts

    def get_bank_account_transactions(
        self,
        bank_account_external_id,
        national_identification_number
    ):
        bank_connection = BankConnections.query.filter_by(
            national_identification_number=national_identification_number
        ).first()

        headers = {
            "Authorization": f"Bearer {bank_connection.access_token}",
            "X-Request-ID": str(uuid4()),
            "Accept": "application/json",
        }
        res = requests.get(
            f"{API_BASE_URL}/{API_ACCOUNTS_ENDPOINT}/{bank_account_external_id}/{API_TRANSACTIONS_ENDPOINT}?bookingStatus=both",
            headers=headers
        )

        transactions_data = res.json()
        now = datetime.datetime.now()

        transaction = BankAccountTransactions(
            id=str(uuid4()),
            external_bank_account_id=bank_account_external_id,
            transactions=json.dumps(transactions_data),
            created_at=now,
            updated_at=now
        )
        self.db.session.add(transaction)
        self.db.session.commit()

        return transaction.serialize()
