from app import create_app
from instance.config import settings
from flask import make_response, jsonify, send_from_directory
import os

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
            "status": 500,
            "message": "Server error encountered"
        }
    ), 500)

@app.errorhandler(400)
def bad_request(err):
    return make_response(jsonify(
        {
            "status": 400,
            "message": "Please provide required information"
        }
    ), 400)

UPLOAD_FOLDER = os.path.abspath("app/uploads")
@app.route('/api/v2/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)