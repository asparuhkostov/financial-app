import sys
import os
from flask import Flask
from requests import requests

sys.path.append("integrations/seb.py")
import SEB

integrations_map = {
    "seb": SEB
}


def create_app(test_config = None):
    app = Flask(__name__)

    @app.route("/connect/<bank>/<personal_id>")
    def connect(bank, personal_id):
        integration = integrations_map[bank]
        integration_instance = integration(personal_id)
        return integration_instance.init_auth()
    
    @app.route("/poll/<bank>/<bank_id_autostart_token>")
    def poll(bank, bank_id_autostart_token):
        integration = integrations_map[bank]
        integration_instance = integration()
        integration_instance.poll_for_bank_id_confirmation(bank_id_autostart_token)

    @app.route("/oauth/<state>")
    def oauth(state):
        return

    return app