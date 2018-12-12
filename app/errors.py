from flask import Blueprint, make_response, jsonify

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def page_not_found(err):
    """Handles all 404 error"""
    return make_response(jsonify(
        {
            "status": 404,
            "message": "Page not found"
        }
    ), 404)
