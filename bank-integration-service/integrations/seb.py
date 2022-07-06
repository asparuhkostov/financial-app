import os
import sys
import requests
from uuid import uuid5


utils_dir = os.getcwd() + "/utils"
sys.path.append(utils_dir)
integrations_dir = os.getcwd() + "/integrations"
sys.path.append(integrations_dir)

from integrations.template import TemplateProvider


SEB_CLIENT_ID = os.environ["SEB_CLIENT_ID"]
SEB_CLIENT_SECRET = os.environ["SEB_CLIENT_SECRET"]


API_BASE_URL = 'https://api-sandbox.sebgroup.com'
API_AUTH_URL = 'auth/v3/authorizations'
API_TOKEN_URL = 'auth/v3/tokens'


def check_for_existing_bank_connection(db_conn, personal_id):
    conn = db_conn.cursor()
    # TO-DO: rewrite this to be safe, this opens the db up to SQL injections as is right now 💀
    res = conn.execute(f'SELECT EXISTS(select 1 from bank_connections where customer_id = {personal_id})')
    conn.close()
    return res


def create_bank_connection(db_conn, personal_id):
    conn = db_conn.cursor()
    bank_conn_id = uuid5()
    # TO-DO: rewrite this to use Alchemy ORM or similar, to avoid SQL injection risks and to improve readability
    conn.execute(f'INSERT INTO \'bank_connections\' VALUES({bank_conn_id}, {personal_id}, NULL, NULL)')
    conn.close()
    return bank_conn_id


def create_authorization_request():
    url = f"{API_BASE_URL}/{API_AUTH_URL}"
    data = {
        "client_id": SEB_CLIENT_ID,
        "scope": "psd2_accounts psd2_payments",
        "start_mode": "ast"
    }
    r = requests.post(url, data)
    d = r.json()
    return d["auth_request_id"]


def get_bankid_autostart_token(auth_req_id):
    r = requests.get(f"{API_BASE_URL}/{API_AUTH_URL}/{auth_req_id}")
    d = r.json()
    return d["autostart_token"]


class SEB(TemplateProvider):
    def init_auth(self, personal_id):
        if check_for_existing_bank_connection(self.db_connection):
            return
        create_bank_connection(self.db_connection, personal_id)
        auth_req_id = create_authorization_request()
        self.db_connection.close()
        return {
            "auth_request_id": auth_req_id,
            "bank_id_autostart_token": get_bankid_autostart_token(auth_req_id)
        }

  
    def check_for_bankid_login_completion(bank_id_autostart_token):
        res = requests.get(f"{API_BASE_URL}/{API_AUTH_URL}")
        if res.json()["status"] == "COMPLETE":
            return True
        else:
            return False


    def get_access_token(auth_req_id):
        data = {
            "client_id": SEB_CLIENT_ID,
            "client_secret": SEB_CLIENT_SECRET,
            "auth_req_id": auth_req_id,
        }
        res = requests.post(f"{API_BASE_URL}/{API_TOKEN_URL}", data)
        return res.json()


        

