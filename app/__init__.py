"""This file contains the create_app function which is a factory
for creating the app
"""
from flask import Flask, make_response, jsonify
from flask_restful import Api
from instance import config
from flask_jwt_extended import JWTManager
from flask_cors import CORS
# Local imports
from .api.v2 import v2
from .errors import errors
from .api.v2.models import RevokeToken


def create_app(config):
    app = Flask(__name__, instance_relative_config=True)
    jwt = JWTManager(app)
    CORS(app, resources={r'*':{"origin" :'*'}})
    @jwt.token_in_blacklist_loader
    def check_if_in_blacklist(decrypt_token):
        jwt_token_id = decrypt_token['jti']
        return RevokeToken().is_jwt_blacklisted(jwt_token_id)
    @jwt.revoked_token_loader
    def revoked_token_callback():
        return make_response(jsonify({
            "message": "Token has been revoked",
            "status": 401
        }),401)

    @jwt.expired_token_loader
    def expired_token_callback():
        return make_response(jsonify({
            'status': 401,
            'message': 'The token has expired'
        }), 401)

    @jwt.invalid_token_loader
    def invalid_token_callback(p):
        return make_response(jsonify({
            'status': 401,
            'message': 'The token entered is invalid'
        }), 401)
    app.config.from_object(config)
    app.register_blueprint(v2)
    app.register_blueprint(errors)
    return app
