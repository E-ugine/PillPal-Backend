from pillpal_app.database import db

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), index=True, nullable=False)  
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), index=True, nullable=False)  
    quantity = db.Column(db.Integer, nullable=False)
    price_per_unit = db.Column(db.Float, nullable=False)
    
    @property
    def total_price(self):
        return self.quantity * self.price_per_unit
    
    def __repr__(self):
        return f"<OrderItem Order {self.order_id} - Product {self.product_id} - Qty {self.quantity}>"
