from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from config import config_options

# Initializing imports
db = SQLAlchemy()
ma = Marshmallow()

def create_app(config_name):
    '''
    Function to initizialize the application creation
    '''

    app = Flask(__name__)

    # Setting up the configuration
    app.config.from_object(config_options[config_name])

    # Initialize the db to the app
    db.init_app(app)
    
    # Initialize the api blueprint
    from .api import api_bp as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    return app
