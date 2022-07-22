from server import db


class BankAccountTransactions(db.Model):
    id = db.Column(db.String, primary_key=True)
    external_id = db.Column(db.String, nullable=False)
    bank_account_id = db.Column(db.String, nullable=False)


    def serialize(self):
        return {
            "id": self.id,
            "external_id": self.external_id,
            "bank_account_id": self.bank_connection_id
        }