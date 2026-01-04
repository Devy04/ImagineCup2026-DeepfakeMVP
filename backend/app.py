from flask import Flask
from flask_cors import CORS
from backend.routes import register_routes


def create_app():
    app = Flask(__name__)
    CORS(app)
    register_routes(app)
    return app
