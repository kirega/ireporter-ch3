"""
this file will include all the view endpoints for the application.
"""
import datetime
import json
from flask import jsonify, make_response, request 
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_jwt_identity, jwt_refresh_token_required,
                                jwt_required)
from flask_restful import Resource

from .models import User, Incident
from .validators import IncidentEditSchema, IncidentSchema, UserSchema


class BaseEndpoint(Resource):
    def __init__(self):
        self.u = User()
        self.i = Incident()

class SignUpEndpoint(BaseEndpoint):
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
                "refresh_token": create_refresh_token(identity=user_data["username"]),
                "access_token": create_access_token(identity=user_data["username"])}
                ),
                201)
        
        return make_response(jsonify({"message": "Username/Email already exists"}), 400)

class LoginEndpoint(BaseEndpoint):
    """ This endpoints handles all login posts  POST /login"""

    def post(self):
        """ Accepts login credentials and return success on succcessful authentication"""

        data = request.get_json(force=True)
        user_data, error = UserSchema(
            only=('username', 'password',)).load(data)
        if error:
            return make_response(jsonify({
                "message": "Missing or invalid field members",
                "required": error}), 400)

        result = self.u.get_user(user_data['username'])
       
        if result == False or result  == None:
            return make_response(jsonify({"message": "Login Failed, User does not exist!"}), 401)

        if self.u.check_encrypted_password(user_data['password'], result['password']):
            return make_response(jsonify({
                "message": "Login Success!",
                "access_token": create_access_token(identity=user_data["username"])}), 200)

        return make_response(jsonify({"message": "Login Failed! Invalid Password"}), 401)

class RefreshTokenEndpoint(Resource):
    """Returns the a new refresh token"""

    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity = current_user)
        return make_response(jsonify({
            'message':"New access token created",
            'access_token': access_token}),
            201)

class AllIncidentsEndpoint(BaseEndpoint):
    """Allows for getting all incidents and posting of any new one"""

    @jwt_required
    def post(self):
        data = request.get_json(force=True)
        incident_data, error = IncidentSchema(
            only=('incidentType','location','comment','images','videos')
        ).load(data)
        if error:
            return make_response(jsonify({
                "message": "Missing or invalid field members",
                "required": error}), 400)

        user = get_jwt_identity()
        createdBy = self.u.get_user(user)['id']
        success = self.i.save(
            incident_data['incidentType'],
            incident_data['comment'],
            incident_data['location'],
            createdBy,
            incident_data['images'],
            incident_data['videos'],
            )
        if success:
            return make_response(jsonify({
                "message": "New incident created"}
                ), 201)
    @staticmethod
    def convert(s):
        if isinstance(s,datetime.datetime):
            return s.__str__()
        
    @jwt_required
    def get(self):
        user = get_jwt_identity()
        createdBy = self.u.get_user(user)['id']
        results = self.i.get_incidents(createdBy)
        if results == False or results is None :
            return make_response(jsonify({"message":"No incidents"}))
        return make_response(jsonify(results), 200)

class IncidentEndpoint(BaseEndpoint):
    @jwt_required
    def get(self,incidentId):
        user = get_jwt_identity()
        createdBy = self.u.get_user(user)['id']
        results = self.i.get_incident(incidentId,createdBy)
        if results == False or results is None :
            return make_response(jsonify({"message":"No incident by that id"}))
        return make_response(jsonify(results), 200)
