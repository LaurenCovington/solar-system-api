from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv # package and object from package that's responsible for org'ing env vars
import os # allows us to read those env vars w a method it offers

db = SQLAlchemy()
migrate = Migrate() 
load_dotenv() # calling this method loads the var envs from the .env file to this file, where the os module can see them

def create_app(test_config=None): # new param is flag that controls whether or not we go into testing or dev env
    app = Flask(__name__)
    # test_config should receive a dictionary of configuration settings. Here, it has default value of None, making the parameter optional
    if not test_config: # check test_config, if it's falsey ('not test_config' means falsey), PC knows it's not running the app in testing mode
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        # os.environ.get() syntax gets an environment variable by the passed-in name
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
            "SQLALCHEMY_DATABASE_URI") # unwanted access blocked
    else: # if test_config is truthy, PC knows we're trying to run the app in test mode
        app.config["TESTING"] = True # actually turns testing mode on
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_TEST_DATABASE_URI")

    db.init_app(app) 
    migrate.init_app(app, db) 

    from models.planet import Planet 
    from .routes import planet_bp
    app.register_blueprint(planet_bp)

    return app 
