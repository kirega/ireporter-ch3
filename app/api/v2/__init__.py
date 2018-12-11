from flask import Blueprint
from flask_restful import Api
from .views import (SignUpEndpoint, LoginEndpoint,
                    RefreshTokenEndpoint, AllIncidentsEndpoint,
                    IncidentEndpoint, IncidentEditCommentEndpoint,
                    IncidentEditLocationEndpoint, AdminStatusEndpoint)

v2 = Blueprint('api', __name__, url_prefix='/api/v2')
api = Api(v2)

api.add_resource(SignUpEndpoint, '/signup')
api.add_resource(LoginEndpoint, '/login')
api.add_resource(AllIncidentsEndpoint, '/incidents')
api.add_resource(IncidentEndpoint, '/incident/<incidentId>')
api.add_resource(IncidentEditCommentEndpoint, '/incident/<incidentId>/comment')
api.add_resource(IncidentEditLocationEndpoint,
                 '/incident/<incidentId>/location')
api.add_resource(AdminStatusEndpoint, '/incident/<incidentId>/status')
api.add_resource(RefreshTokenEndpoint, '/token')
