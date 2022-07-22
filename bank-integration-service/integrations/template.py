class TemplateProvider:
    db = None
    customer_national_identification_number = None


    def __init__(self, db, customer_national_identification_number = None):
        self.db = db
        if customer_national_identification_number:
            self.customer_national_identification_number = customer_national_identification_number


    def init_auth():
        pass


    def verify_login():
        pass


    def create_bank_connection():
        pass


    def refresh_bank_connection():
        pass


    def get_bank_accounts():
        pass


    def get_bank_account_transactions():
        pass


    def initiate_payment():
        pass