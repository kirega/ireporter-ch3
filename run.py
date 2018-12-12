from app import create_app
from instance.config import settings
from flask import make_response, jsonify

app = create_app(settings['production'])

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
