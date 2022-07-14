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


SEB_CLIENT_ID = os.environ["SEB_CLIENT_ID"]
SEB_CLIENT_SECRET = os.environ["SEB_CLIENT_SECRET"]


API_BASE_URL = 'https://api-sandbox.sebgroup.com'
API_AUTH_URL = 'auth/v3/authorizations'
API_TOKEN_URL = 'auth/v3/tokens'


def create_authorization_request():
    url = f"{API_BASE_URL}/{API_AUTH_URL}"
    data = {
        "client_id": SEB_CLIENT_ID,
        "scope": "psd2_accounts psd2_payments",
        "start_mode": "ast"
    }
    r = requests.post(url, json=data)
    d = r.json()
    return d["auth_req_id"]


def get_bankid_autostart_token(auth_req_id):
    r = requests.get(f"{API_BASE_URL}/{API_AUTH_URL}/{auth_req_id}")
    d = r.json()
    return d["autostart_token"]


def get_token_data(auth_req_id):
        data = {
        "client_id": SEB_CLIENT_ID,
        "client_secret": SEB_CLIENT_SECRET,
        "auth_req_id": auth_req_id,
        }
        res = requests.post(f"{API_BASE_URL}/{API_TOKEN_URL}", json=data)
        return res.json()

class SEB(TemplateProvider):
    def init_auth(self):
        auth_req_id = create_authorization_request()
        return {
            "auth_request_id": auth_req_id,
            "bank_id_autostart_token": get_bankid_autostart_token(auth_req_id)
        }

  
    def check_for_login_completion(self, auth_req_id):
        res = requests.get(f"{API_BASE_URL}/{API_AUTH_URL}/{auth_req_id}")
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
        return {"success": True}


        

