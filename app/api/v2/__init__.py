from flask import Blueprint
from flask_restful import Api
from .views import SignUpEndpoint, LoginEndpoint

v2 = Blueprint('api', __name__, url_prefix='/api/v2')
api = Api(v2)

api.add_resource(SignUpEndpoint,'/signup')
api.add_resource(LoginEndpoint,'/login')