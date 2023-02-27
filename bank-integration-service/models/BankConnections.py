from server import db


class BankConnections(db.Model):
    id = db.Column(db.String, primary_key=True)
    bank = db.Column(db.String(120), nullable=False)
    national_identification_number = db.Column(db.String(60), nullable=False)
    access_token = db.Column(db.String(140), nullable=False)
    refresh_token = db.Column(db.String(140), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "bank": self.bank,
            "national_identification_number": self.national_identification_number,
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at)
        }
