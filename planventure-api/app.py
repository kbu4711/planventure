import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from database import db

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure Flask app
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    'sqlite:///planventure.db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False
app.config['ENV'] = os.getenv('FLASK_ENV', 'development')
app.config['DEBUG'] = os.getenv('FLASK_DEBUG', True)

# Initialize CORS
CORS(app)

# Initialize SQLAlchemy with app
db.init_app(app)

# Import models after db initialization to register with SQLAlchemy
from models import User, Trip, ItineraryItem

@app.route('/')
def home():
    return jsonify({"message": "Welcome to PlanVenture API"})

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy"})

@app.route('/api/version')
def version():
    return jsonify({"version": "1.0.0"})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
