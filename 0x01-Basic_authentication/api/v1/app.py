#!/usr/bin/env python3
""" Flask API Application
"""
from flask import Flask
from api.v1.views import app_views
from models import db  # Assuming you're using SQLAlchemy
from api.v1.auth import Auth

# Initialize the Flask app
app = Flask(__name__)

# Configurations for the app (e.g., database, secret key, etc.)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # Example using SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable unnecessary modifications tracking
app.config['SECRET_KEY'] = 'your_secret_key_here'

# Initialize database
db.init_app(app)

# Register the authentication class
auth = Auth()

# Register the blueprint for views
app.register_blueprint(app_views)

# Set up custom error handlers for common HTTP errors
@app.errorhandler(404)
def not_found_error(error):
    """ Custom handler for 404 errors """
    return {"error": "Not Found"}, 404

@app.errorhandler(401)
def unauthorized_error(error):
    """ Custom handler for 401 errors """
    return {"error": "Unauthorized"}, 401

@app.errorhandler(403)
def forbidden_error(error):
    """ Custom handler for 403 errors """
    return {"error": "Forbidden"}, 403

@app.errorhandler(500)
def internal_error(error):
    """ Custom handler for 500 errors """
    return {"error": "Internal Server Error"}, 500

# Set up the route for the status endpoint
@app.route('/api/v1/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """ GET /api/v1/status
    Return:
      - the status of the API
    """
    return {"status": "OK"}, 200

# Set up the route for the stats endpoint
@app.route('/api/v1/stats/', strict_slashes=False)
def stats() -> str:
    """ GET /api/v1/stats
    Return:
      - the number of each object
    """
    from models.user import User
    stats = {}
    stats['users'] = User.count()  # Assuming the User model has a count method
    return stats, 200

# Set up the route for unauthorized access (forbidden endpoint)
@app.route('/api/v1/unauthorized', methods=['GET'], strict_slashes=False)
def unauthorized() -> None:
    """ GET /api/v1/unauthorized
    Raise:
      - a 401 error
    """
    return {"error": "Unauthorized"}, 401

# Set up the route for forbidden access (forbidden endpoint)
@app.route('/api/v1/forbidden', methods=['GET'], strict_slashes=False)
def forbidden() -> None:
    """ GET /api/v1/forbidden
    Raise:
      - a 403 error
    """
    return {"error": "Forbidden"}, 403

# Main entry point to run the app
if __name__ == "__main__":
    # Run the application
    app.run(host="0.0.0.0", port=5000, debug=True)
