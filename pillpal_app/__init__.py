from flask import Flask
from flask_migrate import Migrate
from pillpal_app.config import CoolConfig
from pillpal_app.database import db
from pillpal_app.routes.main_route import main_blueprint
from pillpal_app.routes.user_routes import user_blueprint
from pillpal_app.routes.product_routes import product_blueprint
from pillpal_app.routes.order_routes import order_blueprint

def create_app():    
    # Initialize Flask app
    app = Flask(__name__)        

    # App Configuration
    app.config.from_mapping(
        SECRET_KEY="My_Secret_Key"
    )     
    app.config.from_object(CoolConfig)    

    # Initialize Extensions
    db.init_app(app)
    Migrate(app, db)

    # Import models for migrations
    from pillpal_app.models.user import User
    from pillpal_app.models.product import Product
    from pillpal_app.models.order import Order
    from pillpal_app.models.order_item import OrderItem
    from pillpal_app.models.payment import Payment

    # Register Blueprints
    app.register_blueprint(main_blueprint, url_prefix='/')
    app.register_blueprint(user_blueprint, url_prefix='/api/users')
    app.register_blueprint(product_blueprint, url_prefix='/api/products')
    app.register_blueprint(order_blueprint, url_prefix='/api/orders')

    # Return the app instance
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
