from flask import Flask
from .config import Config
from .db import db,migrate
from .models import *
from .routes import fitting_bp, authentication_bp
from flask_bcrypt import Bcrypt

bcrypt=Bcrypt()

def create_app():
    app=Flask(__name__)
    app.config.from_object(Config)

    # initialize db
    db.init_app(app)
    migrate.init_app(app,db)

    # initialize bcrypt
    bcrypt.init_app(app)


    # register blueprint
    app.register_blueprint(fitting_bp)
    app.register_blueprint(authentication_bp)
    # Can also have the url_prefix here
    # app.register_blueprint(fitting_bp,url_prefix="/fitting")

    return app