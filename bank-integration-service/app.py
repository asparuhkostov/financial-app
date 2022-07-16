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

@app.route("/check/<bank>/<auth_req_id>")
def check(bank, auth_req_id):
    integration = integrations_map[bank]
    integration_instance = integration(db)
    return integration_instance.check_for_login_completion(auth_req_id)

@app.route("/create_bank_connection/<bank>/<auth_req_id>/customer_national_identification_number")
def create_bank_connection(bank, auth_req_id, customer_national_identification_number):
    integration = integrations_map[bank]
    integration_instance = integration(db, customer_national_identification_number)
    connection_id = integration_instance.create_bank_connection(auth_req_id)
    return {"success": True if connection_id else False}

@app.route("/get_bank_accounts/<bank>/<customer_national_identification_number>")
def get_bank_accounts(bank, customer_national_identification_number):
    integration = integrations_map[bank]
    integration_instance = integration(db, customer_national_identification_number)
    return integration_instance.get_accounts()

app.run(debug = True)