from server import db


class BankAccounts(db.Model):
    id = db.Column(db.String, primary_key=True)
    external_id = db.Column(db.String, nullable=False)
    bank_connection_id = db.Column(db.String, nullable=False)
    bank = db.Column(db.String, nullable=False)
    name = db.Column(db.String)
    iban = db.Column(db.String)
    currency = db.Column(db.String)


    def serialize(self):
        return {
            "id": self.id,
            "external_id": self.external_id,
            "bank_connection_id": self.bank_connection_id,
            "bank": self.bank,
            "name": self.name,
            "iban": self.iban,
            "currency": self.currency
        }