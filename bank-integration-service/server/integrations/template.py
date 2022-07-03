import os
import psycopg2

DB_HOST = os.getenv("DB_HOST")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

class TemplateProvider:
    def __init__(self, personal_id):
        self.personal_id = personal_id
        self.db_connection = psycopg2.connect(f'host={DB_HOST} dbname={DB_NAME} user={DB_USERNAME} password={DB_PASSWORD}')

    def init_auth():
        pass

    def get_access_token():
        pass

    def get_refresh_token():
        pass
    
    def get_accounts():
        pass

    def get_account_transactions():
        pass

    def initiate_payment():
        pass