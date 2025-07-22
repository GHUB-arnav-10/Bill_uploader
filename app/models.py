from app import db
from datetime import datetime

class Receipt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vendor = db.Column(db.String(150), nullable=False, index=True)
    transaction_date = db.Column(db.Date, nullable=False, index=True)
    amount = db.Column(db.Float, nullable=False, index=True)
    category = db.Column(db.String(100), nullable=True, index=True)
    file_name = db.Column(db.String(200), nullable=False)
    uploaded_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return f'<Receipt {self.vendor} - ${self.amount}>'

    def to_dict(self):
        return {
            'id': self.id,
            'vendor': self.vendor,
            'transaction_date': self.transaction_date.isoformat(),
            'amount': self.amount,
            'category': self.category,
            'file_name': self.file_name,
            'uploaded_at': self.uploaded_at.isoformat()
        }
