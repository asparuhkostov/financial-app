import sys
import os


from flask import Response


sys.path.append(f'{os.getcwd()}/server')
from server import app, db
sys.path.append(f'{os.getcwd()}/server/integrations')
from integrations.seb import SEB


integrations_map = {
    "seb": SEB
}


@app.route("/health")
def hello_world():
    return Response(status=200)


@app.route("/connect/<bank>")
def connect(bank):
    integration = integrations_map[bank]
    integration_instance = integration(db)
    return integration_instance.init_auth()


@app.route("/verify_login/<bank>/<auth_req_id>")
def verify_login(bank, auth_req_id):
    integration = integrations_map[bank]
    integration_instance = integration(db)
    return integration_instance.verify_login(auth_req_id)


@app.route("/create_bank_connection/<bank>/<auth_req_id>/<customer_national_identification_number>")
def create_bank_connection(bank, auth_req_id, customer_national_identification_number):
    integration = integrations_map[bank]
    integration_instance = integration(db, customer_national_identification_number)
    return integration_instance.create_bank_connection(auth_req_id)


@app.route("/refresh_bank_connection/<bank>/<customer_national_identification_number>")
def refresh_bank_connection(bank, customer_national_identification_number):
    integration = integrations_map[bank]
    integration_instance = integration(db, customer_national_identification_number)
    return integration_instance.refresh_bank_connection()


@app.route("/get_bank_accounts/<bank>/<customer_national_identification_number>")
def get_bank_accounts(bank, customer_national_identification_number):
    integration = integrations_map[bank]
    integration_instance = integration(db, customer_national_identification_number)
    return integration_instance.get_bank_accounts()


@app.route("/get_bank_account_transactions/<bank>/<customer_national_identification_number>/bank_account_external_id")
def get_bank_account_transactions(bank, customer_national_identification_number, bank_account_external_id):
    integration = integrations_map[bank]
    integration_instance = integration(db, customer_national_identification_number)
    return integration_instance.get_bank_account_transactions(bank_account_external_id)


app.run(host="0.0.0.0", debug = True)