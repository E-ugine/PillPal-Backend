from pillpal_app.database import db
from datetime import datetime
from sqlalchemy import Enum
from enum import Enum as PyEnum

class OrderStatus(PyEnum):
    PENDING = 'pending'
    DELIVERED='delivered'
    CANCELED ='canceled'

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) 
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default="pending")  # pending, delivered, canceled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    order_items = db.relationship('OrderItem', backref='order', lazy=True)
    payment = db.relationship('Payment', backref='order', uselist=False, lazy=True)  # One-to-One relationship
    
    def __repr__(self):
        return f"<Order {self.id} - User {self.user_id} - ${self.total_amount}>"