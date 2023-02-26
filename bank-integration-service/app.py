from integrations.seb import SEB
from lib.Aggregator import Aggregator


from flask import Response, request
from server import app, db


import sys
import os


sys.path.append(f'{os.getcwd()}/server')
sys.path.append(f'{os.getcwd()}/server/integrations')
sys.path.append(f'{os.getcwd()}/lib')


integrations_map = {
    "seb": SEB
}


@app.get("/health")
def hello_world():
    return Response(status=200)


@app.post("/start_login")
def start_login():
    request_data = request.json
    bank = request.json["bank"]
    integration = integrations_map[bank]
    integration_instance = integration(db)

    return integration_instance.init_auth()


@app.post("/verify_login")
def verify_login():
    request_data = request.json
    bank = request_data["bank"]
    auth_req_id = request_data["auth_req_id"]

    integration = integrations_map[bank]
    integration_instance = integration(db)

    return integration_instance.verify_login(
        auth_req_id
    )


@app.post("/connection")
def create_bank_connection():
    request_data = request.json
    bank = request_data["bank"]
    auth_req_id = request_data["auth_req_id"]
    national_identification_number = request_data["national_identification_number"]

    integration = integrations_map[bank]
    integration_instance = integration(
        db=db
    )

    # TO-DO - make sure that users cannot have more than 1
    # connections per bank
    return integration_instance.create_bank_connection(
        auth_req_id,
        national_identification_number
    )


@app.put("/connection")
def refresh_bank_connection():
    request_data = request.json
    bank = request_data["bank"]
    national_identification_number = request_data[
        "national_identification_number"]

    integration = integrations_map[bank]
    integration_instance = integration(
        db=db
    )

    return integration_instance.refresh_bank_connection(
        national_identification_number
    )


@app.get("/populate_financial_information_records/<bank>/<national_identification_number>")
def populate(bank, national_identification_number):
    integration = integrations_map[bank]
    integration_instance = integration(
        db=db
    )
    accounts = integration_instance.get_bank_accounts(
        national_identification_number)
    for a in accounts:
        integration_instance.get_bank_account_transactions(
            a["external_id"],
            national_identification_number
        )

    return Response(status=200)


@ app.get("/get_financial_records/<national_identification_number>")
def get_financial_records(national_identification_number):
    aggregator = Aggregator(national_identification_number)
    financial_information = aggregator.compile_financial_information()

    return financial_information


app.run(host="0.0.0.0", debug=True)
