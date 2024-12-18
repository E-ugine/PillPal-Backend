from pillpal_app.database import db
from datetime import datetime
from sqlalchemy import Enum
from enum import Enum as PyEnum

class PaymentStatus(PyEnum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"

class Payment(db.Model):
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), unique=True, index=True, nullable=False)  # One-to-One with Order
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)  
    payment_status = db.Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
    transaction_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Payment Order {self.order_id} - ${self.amount} - {self.payment_status}>"
