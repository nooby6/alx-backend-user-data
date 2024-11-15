#!/usr/bin/env python3
""" Module of Index views
"""
from flask import Flask, jsonify, abort
from api.v1.views import app_views
from models.user import User

# Initialize the Flask app
app = Flask(__name__)

# Register the blueprint
app.register_blueprint(app_views)

# Set up the route for the status endpoint
@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """ GET /api/v1/status
    Return:
      - the status of the API
    """
    return jsonify({"status": "OK"})

# Set up the route for the stats endpoint
@app_views.route('/stats/', strict_slashes=False)
def stats() -> str:
    """ GET /api/v1/stats
    Return:
      - the number of each object
    """
    stats = {}
    stats['users'] = User.count()  # Assuming the User model has a count method
    return jsonify(stats)

# Set up the route for the unauthorized endpoint
@app_views.route('/unauthorized', methods=['GET'], strict_slashes=False)
def unauthorized() -> None:
    """ GET /api/v1/unauthorized
    Raise:
      - a 401 error
    """
    abort(401)

# Set up the route for the forbidden endpoint
@app_views.route('/forbidden', methods=['GET'], strict_slashes=False)
def forbidden() -> None:
    """ GET /api/v1/forbidden
    Raise:
      - a 403 error
    """
    abort(403)

# Handle 404 errors
@app.errorhandler(404)
def not_found_error(error):
    """ Custom handler for 404 errors """
    return jsonify({"error": "Not Found"}), 404

# Handle 401 errors
@app.errorhandler(401)
def unauthorized_error(error):
    """ Custom handler for 401 errors """
    return jsonify({"error": "Unauthorized"}), 401

# Handle 403 errors
@app.errorhandler(403)
def forbidden_error(error):
    """ Custom handler for 403 errors """
    return jsonify({"error": "Forbidden"}), 403

# Handle internal server errors (500)
@app.errorhandler(500)
def internal_error(error):
    """ Custom handler for 500 errors """
    return jsonify({"error": "Internal Server Error"}), 500

# Main entry point to run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
