from pillpal_app.database import db
from pillpal_app.models.user import User
from datetime import datetime
from sqlalchemy.orm import validates
class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    stock_quantity = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @validates('price')
    def validates_price(self, key, price):
        if price < 0:
            raise ValueError('Price must be non-negative')
        return price
    

    
    def __repr__(self):
        return f"<Product {self.name} - ${self.price}>"