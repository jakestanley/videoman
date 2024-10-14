from flask_cors import CORS

def setup_cors(app):
    CORS(app, origins=["http://localhost:5000", "http://localhost:8080", "http://localhost:5173"])