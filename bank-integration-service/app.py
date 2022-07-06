import sys
import os
from flask import Flask


sys.path.append(f'{os.getcwd()}/server/integrations')
from integrations.seb import SEB


integrations_map = {
    "seb": SEB
}


def create_app(test_config = None):
    app = Flask(__name__)

    @app.route("/connect/<bank>")
    def connect(bank):
        integration = integrations_map[bank]
        integration_instance = integration()
        return integration_instance.init_auth()
    
    @app.route("/check/<bank>/<auth_req_id>")
    def check(bank, auth_req_id):
        integration = integrations_map[bank]
        integration_instance = integration()
        return integration_instance.check_for_login_completion(auth_req_id)
    
    @app.route("/get_access_token/<bank>/<auth_req_id>")
    def get_access_token(bank, auth_req_id):
        integration = integrations_map[bank]
        integration_instance = integration()
        return integration_instance.get_access_token(auth_req_id)

    @app.route("/oauth/<state>")
    def oauth(state):
        return

    return app