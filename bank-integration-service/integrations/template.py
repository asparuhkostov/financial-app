class TemplateProvider:
    db = None
    customer_national_identification_number = None

    def __init__(self, db, customer_national_identification_number = None):
        self.db = db
        if customer_national_identification_number:
            self.customer_national_identification_number = customer_national_identification_number
    
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