from flask import Flask
from flask_migrate import Migrate
from pillpal_app.models import user, product
from pillpal_app.config import CoolConfig
from pillpal_app.database import db

def create_app():    
    # Initialize Flask app
    app = Flask(__name__)        

    # App Configuration
    app.config.from_mapping(
        SECRET_KEY="My_Secret_Key"
    )     
    app.config.from_object(CoolConfig)    

    db.init_app(app)
    migrate = Migrate(app, db)

    from pillpal_app.models.user import User
    from pillpal_app.models.product import Product
    from pillpal_app.models.order import Order
    from pillpal_app.models.order_item import OrderItem
    from pillpal_app.models.payment import Payment
    
   
    return app
