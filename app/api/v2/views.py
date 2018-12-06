"""
this file will include all the view endpoints for the application.
"""

from flask import make_response, jsonify, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from .models import User
from .validators import (UserSchema, IncidentSchema,
                         IncidentEditSchema)


class BaseAuthEndpoint(Resource):
    def __init__(self):
        self.u = User()


class SignUpEndpoint(BaseAuthEndpoint):
    """
    A resource that provides the endpoint POST /signup.

    """

    def post(self):
        """
        Registers new users based on data sent
        """
        data = request.get_json(force=True)
        user_data, error = UserSchema().load(data)

        if error:
            return make_response(jsonify({
                "message": "Missing or invalid field members",
                "required": error}), 400)

        success = self.u.save(
            user_data["first_name"],
            user_data["last_name"],
            user_data["other_names"],
            user_data["phonenumber"],
            user_data["email"],
            user_data["username"],
            user_data["password"]
        )
        if success:
            return make_response(jsonify({
                "message": "Sign Up successful. Welcome!",
                "access_token": create_access_token(identity=user_data["username"])}),
                201)
        
        return make_response(jsonify({"message": "Username/Email already exists"}), 400)

