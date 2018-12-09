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


@errors.app_errorhandler(500)
def server_error(err):
    return make_response(jsonify(
        {
            "status": 500,
            "message": "An exception occured, server error"
        }
    ), 500)

@errors.app_errorhandler(405)
def method_not_allowed(err):
    return make_response(jsonify(
        {
            "status": 405,
            "message": "Method is not allowed"
        }
    ), 405)
