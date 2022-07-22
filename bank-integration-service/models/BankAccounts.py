from server import db

class BankAccounts(db.Model):
    id = db.Column(db.String, primary_key=True)
    bank_connection_id = db.Column(db.String, nullable=False)
    bank = db.Column(db.String, nullable=False)
    name = db.Column(db.String)
    iban = db.Column(db.String)
    currency = db.Column(db.String)