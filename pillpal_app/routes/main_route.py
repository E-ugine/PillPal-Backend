from flask import Blueprint

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/')
def home():
    return 'Welcome To The PillPal API'
