from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from src.routes.login import api
from flask_session import Session
from src.routes.search import search_bp
import os
import requests


# Initialize the Flask app
app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("CLIENT_ID")  # Replace with a strong secret key
app.config["SESSION_TYPE"] = "filesystem"  # For production, use Redis or another backend
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SECURE"] = True  # Use HTTPS
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
Session(app)# Initialize Flask-Session


# Register the blueprint
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(search_bp, url_prefix='/api')  # Register the search Blueprint


# After request: Set headers to prevent browser caching
@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.route("/")
def index():
    return render_template("index.html")

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=os.getenv("FLASK_DEBUG", "false").lower() == "true")
