"""
this file will include all the view endpoints for the application.
"""
import os
import datetime
import json
from flask import jsonify, make_response, request, url_for, send_from_directory
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_jwt_identity, jwt_refresh_token_required,
                                jwt_required, get_raw_jwt)
from flask_restful import Resource
from werkzeug.utils import secure_filename
from .models import User, Incident, RevokeToken
from .validators import IncidentEditSchema, IncidentSchema, UserSchema

# UPLOAD_FOLDER = '/app/uploads'
UPLOAD_FOLDER = os.path.abspath("app/uploads")
ALLOWED_EXTENSIONS = set(['mp4', 'png', 'jpg', 'jpeg'])


class BaseEndpoint(Resource):
    def __init__(self):
        self.u = User()
        self.i = Incident()

    @staticmethod
    def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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

        if 'isAdmin' in user_data:
            success = self.u.save(
                user_data["first_name"],
                user_data["last_name"],
                user_data["other_names"],
                user_data["phonenumber"],
                user_data["email"],
                user_data["username"],
                user_data["password"],
                user_data["isAdmin"]
            )
        else:
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
                "message": "Sign Up successful. Welcome!"}
            ), 201)

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

        if result == False or result == None:
            return make_response(jsonify({"message": "Login Failed, Incorrect Username/Password!"}), 401)

        if self.u.check_encrypted_password(user_data['password'], result['password']):
            return make_response(jsonify({
                "message": "Login Success!",
                "refresh_token": create_refresh_token(identity=user_data["username"]),
                "access_token": create_access_token(identity=user_data["username"], expires_delta=False)}), 200)

        return make_response(jsonify({"message": "Login Failed, Incorrect Username/Password!"}), 401)


class LogoutEndpoint(BaseEndpoint):
    """ This endpoint handles User logout and blacklisting of that access token"""
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        if RevokeToken().add(jti):
            return make_response(jsonify({
                "message": "Successfully logged out!",
                "status": 200
            }), 200)


class RefreshTokenEndpoint(Resource):
    """Returns the a new refresh token"""

    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return make_response(jsonify({
            'message': "New access token created",
            'access_token': access_token}),
            201)


class AllIncidentsEndpoint(BaseEndpoint):
    """Allows for getting all incidents and posting of any new one"""

    @jwt_required
    def post(self):
        """Endpoint POST /incidents
        Allows creation of new incidents"""
        if request.form:
            data = request.form
        else:
            data = json.loads(request.data)
        incident_data, error = IncidentSchema(
            only=('incidentType', 'location', 'comment',)
        ).load(data)
        if error:
            return make_response(jsonify({
                "message": "Missing or invalid field members",
                "required": error}), 400)

        user = get_jwt_identity()
        createdBy = self.u.get_user(user)['id']
        videos = []
        images = []
        if 'image' in request.files:
            files = request.files.getlist('image')
            for file in files:
                if file and self.allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(UPLOAD_FOLDER, filename))
                    images.append(url_for('uploaded_file', filename=filename))

        if 'video' in request.files:
            files = request.files.getlist('video')
            for file in files:
                if file and self.allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(UPLOAD_FOLDER, filename))
                    if filename.rsplit('.', 1)[1].lower() == 'mp4':
                        videos.append(
                            url_for('uploaded_file', filename=filename))
                            
        success = self.i.save(
            incident_data['incidentType'],
            incident_data['comment'],
            incident_data['location'],
            createdBy,
            images,
            videos,
        )
        if success:
            return make_response(jsonify({
                "message": "New incident created",
                "status": 201}
            ), 201)

        return make_response(jsonify({
            "message": "Incident can only be red-flag/intervention",
            "status": 400}), 400)

    @jwt_required
    def get(self):
        """Endpoint GET /incidents.
        Returns list of all incidents"""

        user = get_jwt_identity()
        createdBy = self.u.get_user(user)['id']
        isAdmin = self.u.get_user(user)['isadmin']
        if isAdmin:
            results = self.i.get_all()
        else:
            results = self.i.get_incidents(createdBy)
        if results == False or results is None:
            return make_response(jsonify({"message": "No incidents"}))
        return make_response(jsonify(results), 200)


class IncidentEndpoint(BaseEndpoint):
    @jwt_required
    def get(self, incidentId):
        """
        GET /incident/<incidentId>
        Returns a single instance
        """
        try:
            incidentId = int(incidentId)
        except ValueError:
            return make_response(jsonify({
                "message": "Failed! incidentId is not an id",
                "status": 400
            }), 400)

        user = get_jwt_identity()
        createdBy = self.u.get_user(user)['id']
        results = self.i.get_incident(incidentId, createdBy)
        if results == False or results is None:
            return make_response(jsonify({
                "message": "No incident by that id/ Not owned",
                "status": 404
            }), 404)
        return make_response(jsonify(results), 200)

    @jwt_required
    def delete(self, incidentId):
        """
        DELETE /incident/<incidentId>
        deletes a single instance
        """
        try:
            incidentId = int(incidentId)
        except ValueError:
            return make_response(jsonify({
                "message": "Failed! incidentId is not an id",
                "status": 400}), 400)

        user = get_jwt_identity()
        createdBy = self.u.get_user(user)['id']
        exists_owned = self.i.get_incident(incidentId, createdBy)

        if exists_owned == False or exists_owned is None:
            return make_response(jsonify({"message": "Forbiden cannot delete,record may not exist",
                                          "status": 403}), 403)

        result = self.i.delete(incidentId, createdBy)
        if result:
            return make_response(jsonify({
                "message": "Incident record has been deleted",
                "status": 200}
            ), 200)


class IncidentEditCommentEndpoint(BaseEndpoint):
    """
    Endpoint PUT /incident/1/comment
    Allows for editing the comment on an incident
    """
    @jwt_required
    def put(self, incidentId):
        """Allows for editing the comment on an incident"""
        try:
            incidentId = int(incidentId)
        except ValueError:
            return make_response(jsonify({
                "message": "Failed! incidentId is not an id",
                "status": 400}), 400)

        user = get_jwt_identity()
        createdBy = self.u.get_user(user)['id']
        data = request.get_json(force=True)
        incident_data = IncidentEditSchema(
            only=('comment',)).load(data)
        if incident_data.errors:
            return make_response(jsonify({
                "message": "Comment is not present",
                "status": 400,
                "required": incident_data.errors}),
                400)

        exists_owned = self.i.validate_edit(incidentId, createdBy)

        if exists_owned == False or exists_owned is None:
            return make_response(jsonify({
                "message": "Forbidden: Record not owned/ Not in draft status"}), 403)

        edit = self.i.edit_comment(incidentId, data['comment'], createdBy)
        if edit == True:
            return make_response(jsonify({
                'message': "Incident Updated",
            }), 200)

        return make_response(jsonify({
            "message": "Cannot update a record at the moment"}), 403)


class IncidentEditLocationEndpoint(BaseEndpoint):
    """
    Endpoint PUT /incident/1/location
    Allows for editing the location on an incident
    """
    @jwt_required
    def put(self, incidentId):
        """  Allows for editing the location on an incident"""
        try:
            incidentId = int(incidentId)
        except ValueError:
            return make_response(jsonify({"message": "Failed! incidentId is not an id"}), 400)
        user = get_jwt_identity()
        createdBy = self.u.get_user(user)['id']
        data = request.get_json(force=True)
        incident_data = IncidentEditSchema(
            only=('location',)).load(data)
        if incident_data.errors:
            return make_response(jsonify({
                "message": "location is not present",
                "required": incident_data.errors}),
                400)

        exists_owned = self.i.validate_edit(incidentId, createdBy)

        if exists_owned == False or exists_owned is None:
            return make_response(jsonify({
                "message": "Forbidden: Record not owned/ Not in draft status"}), 403)

        edit = self.i.edit_location(incidentId, data['location'], createdBy)
        if edit == True:
            return make_response(jsonify({
                'message': "Incident Updated",
            }), 200)

        return make_response(jsonify({
            "message": "Cannot update a record at the moment"}), 403)


class AdminStatusEndpoint(BaseEndpoint):

    """
    Endpoint PUT /incident/status
    Allows for and admin to update the status of a record
    """
    @jwt_required
    def put(self, incidentId):
        try:
            incidentId = int(incidentId)
        except ValueError:
            return make_response(jsonify({"message": "Failed! incidentId is not an id"}), 400)
        data = request.get_json(force=True)
        incident_data = IncidentEditSchema(
            only=('status',)).load(data)

        if incident_data.errors:
            return make_response(jsonify({
                "message": "status is not present",
                "required": incident_data.errors}),
                400)
        user = get_jwt_identity()

        isAdmin = self.u.get_user(user)['isadmin']

        if isAdmin == True:
            update = self.i.update_status(incidentId, data['status'])
        else:
            return make_response(jsonify({
                "message": "Incident does not exist/ Not Admin"
            }), 401)

        if update == True:
            return make_response(jsonify({
                'message': 'Incident status updated',
                'status': 200}),
                200)
        return make_response(jsonify({
            "message": "Status can only be draft,under-investigation,resolved or rejected",
        }), 400)
