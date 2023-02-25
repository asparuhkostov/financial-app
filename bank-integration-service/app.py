from integrations.seb import SEB
from server import app, db
import sys
import os


from flask import Response, request


sys.path.append(f'{os.getcwd()}/server')
sys.path.append(f'{os.getcwd()}/server/integrations')


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

    return integration_instance.verify_login(auth_req_id)


@app.post("/connection")
def create_bank_connection():
    request_data = request.json
    bank = request_data["bank"]
    auth_req_id = request_data["auth_req_id"]
    national_identification_number = request_data[
        "national_identification_number"]

    integration = integrations_map[bank]
    integration_instance = integration(db, national_identification_number)

    # TO-DO - make sure that users cannot have more than 1
    # connections per bank
    return integration_instance.create_bank_connection(auth_req_id)


@app.put("/connection")
def refresh_bank_connection():
    request_data = request.json
    bank = request_data["bank"]
    national_identification_number = request_data[
        "national_identification_number"]

    integration = integrations_map[bank]
    integration_instance = integration(db, national_identification_number)

    return integration_instance.refresh_bank_connection()


@app.get("/populate_financial_information_records/bank>/<national_identification_number>")
def populate(bank, national_identification_number):
    integration = integrations_map[bank]
    integration_instance = integration(db, national_identification_number)
    integration_instance.get_bank_accounts()
    integration_instance.get_bank_account_transactions(
        bank_account_external_id)

    return Response(status=200)


@ app.get("/get_financial_records/<national_identification_number>")
def get_financial_records(national_identification_number):
    financial_information = {}
    connections = BankConnections.query.filter_by(
        national_identification_number=self.national_identification_number
    )
    for c in connections:
        accounts = BankAccount.query.filter_by(bank_connection_id=c.id)
        for a in accounts:
            transactions = BankAccountTransactions.query.filter_by(
                bank_account_id=a.id)
            serialised_transactions = []
            for t in transactions:
                serialised_transactions.append(t.serialize())

            account_data = {
                account: a.serialize(),
                transactions: serialised_transactions.
            }
            if a.bank in financial_information:
                financial_information[a.bank].append(account_data)
            else:
                financial_information[a.bank] = [
                    account_data
                ]

    return financial_information


app.run(host="0.0.0.0", debug=True)
