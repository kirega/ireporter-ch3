"""This file contains the create_app function which is a factory
for creating the app
"""
from flask import Flask
from flask_restful import Api
from instance import config
from flask_jwt_extended import JWTManager
# Local imports
from .api.v2 import v2
from .errors import errors


def create_app(config):
    app = Flask(__name__, instance_relative_config=True)
    jwt = JWTManager(app)
    app.config.from_object(config)
    app.register_blueprint(v2)
    app.register_blueprint(errors)
    return app
