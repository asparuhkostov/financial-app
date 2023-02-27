from server import db


class BankAccountTransactions(db.Model):
    id = db.Column(db.String, primary_key=True)
    external_bank_account_id = db.Column(db.String, nullable=False)
    transactions = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "external_bank_account_id": self.external_bank_account_id,
            "transactions": self.transactions,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at)
        }
