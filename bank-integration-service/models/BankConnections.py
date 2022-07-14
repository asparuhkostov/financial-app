from server import db

class BankConnections(db.Model):
    id = db.Column(db.String, primary_key=True)
    bank = db.Column(db.String(120), nullable=False)
    customer_national_identification_number = db.Column(db.String(60), nullable=False)
    access_token = db.Column(db.String(140), nullable=False)
    refresh_token = db.Column(db.String(140), nullable=False)