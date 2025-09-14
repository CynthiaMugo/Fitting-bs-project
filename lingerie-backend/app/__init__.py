from flask import Flask
from .config import Config
from .db import db,migrate
from .models import *
from .routes import fitting_bp

def create_app():
    app=Flask(__name__)
    app.config.from_object(Config)

    # initialize db
    db.init_app(app)
    migrate.init_app(app,db)

    # register blueprint
    app.register_blueprint(fitting_bp)
    # Can also have the url_prefix here
    # app.register_blueprint(student_bp,url_prefix="/student")

    return app