from app import create_app
from instance.config import settings
from flask import make_response, jsonify
from flask_jwt_extended import JWTManager

app =  create_app(settings['testing'])

if __name__ == '__main__':
    app.run()

@app.errorhandler(404)
def page_not_found(err):
    """Handles all 404 error"""
    return make_response(jsonify(
        {
            "status": 404,
            "message": "Page not found"
        }
    ), 404)

@app.errorhandler(405)
def method_not_allowed(err):
    return make_response(jsonify(
        {
            "status": 405,
            "message": "Method is not allowed"
        }
    ), 405)

@app.errorhandler(500)
def server_error(err):
    return make_response(jsonify(
        {
            "status": 405,
            "message": "Server error encountered"
        }
    ), 405)

jwt =  JWTManager(app)

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