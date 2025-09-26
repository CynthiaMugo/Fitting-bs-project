from flask import Flask
from .config import Config
from .db import db,migrate
from .models import *
from .routes import fitting_bp, authentication_bp, order_bp, user_bp
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from datetime import timedelta
from flask_cors import CORS

bcrypt=Bcrypt()
jwt=JWTManager()

def create_app():
    app=Flask(__name__)
    app.config.from_object(Config)
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

    CORS(app)

    # initialize db
    db.init_app(app)
    migrate.init_app(app,db)

    # initialize bcrypt
    bcrypt.init_app(app)

    # initialize jwt
    jwt.init_app(app)

    # register blueprint
    app.register_blueprint(fitting_bp)
    app.register_blueprint(authentication_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(user_bp)
    # Can also have the url_prefix here
    # app.register_blueprint(fitting_bp,url_prefix="/fitting")

    return app