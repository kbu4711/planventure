import os
from flask import Flask, jsonify, g
from flask_cors import CORS
from dotenv import load_dotenv
from database import db
from jwt_utils import setup_jwt
from auth_middleware import protected_route, optional_auth, get_current_user_id

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

# Initialize JWT
jwt = setup_jwt(app)

# Import models after db initialization to register with SQLAlchemy
from models import User, Trip, ItineraryItem

# Import and register blueprints
from routes import auth_bp, trips_bp
app.register_blueprint(auth_bp)
app.register_blueprint(trips_bp)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to PlanVenture API"})

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy"})

@app.route('/api/version')
def version():
    return jsonify({"version": "1.0.0"})


# ============================================================================
# PROTECTED ROUTE EXAMPLES
# ============================================================================

@app.route('/api/me')
@protected_route
def get_current_user():
    """
    Get current authenticated user information.
    
    Requires: Valid JWT token in Authorization header
    
    Example:
        GET /api/me
        Authorization: Bearer <token>
    """
    user_id = get_current_user_id()
    from models.user import User as UserModel
    
    user = UserModel.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'user_not_found', 'message': 'User not found'}), 404
    
    return jsonify({
        'data': {
            'id': user.id,
            'email': user.email,
            'created_at': user.created_at.isoformat()
        }
    }), 200


@app.route('/api/protected-test')
@protected_route
def protected_test():
    """
    Example protected route - requires valid JWT token.
    
    Requires: Valid JWT token in Authorization header
    """
    user_id = get_current_user_id()
    
    return jsonify({
        'message': f'You are authenticated! User ID: {user_id}',
        'user_id': user_id
    }), 200


@app.route('/api/optional-test')
@optional_auth
def optional_test():
    """
    Example route that works with or without authentication.
    
    If authenticated: Shows user info
    If not authenticated: Shows anonymous message
    """
    user_id = get_current_user_id()
    
    if user_id:
        return jsonify({
            'message': f'Authenticated request',
            'user_id': user_id
        }), 200
    else:
        return jsonify({
            'message': 'Anonymous request (no authentication required)'
        }), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
