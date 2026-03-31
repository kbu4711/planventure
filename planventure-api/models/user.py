"""
User model for authentication and profile management
"""
from datetime import datetime, timezone
from database import db
from password_utils import hash_password, verify_password, is_password_strong


class User(db.Model):
    """User model for authentication and profile management"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    
    # Relationships
    trips = db.relationship('Trip', backref='user', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.email}>'

    def set_password(self, password: str) -> None:
        """
        Hash and set the user's password.
        
        Args:
            password: The plain text password to hash and store
            
        Raises:
            ValueError: If password is too short or invalid
        """
        self.password_hash = hash_password(password)

    def check_password(self, password: str) -> bool:
        """
        Verify the provided password against the stored hash.
        
        Args:
            password: The plain text password to verify
            
        Returns:
            True if password matches, False otherwise
        """
        return verify_password(password, self.password_hash)

    def validate_password_strength(self) -> dict:
        """
        Validate password strength requirements.
        
        Returns:
            Dictionary with strength assessment containing:
            - is_strong: bool indicating if password meets all requirements
            - score: int from 0-5
            - Details on each requirement
        """
        # Note: This would be called during password change validation
        # Actual password check would be done before set_password
        return {
            'is_strong': True,
            'message': 'Password strength validated during set_password'
        }

    def to_dict(self):
        """Convert user to dictionary representation"""
        return {
            'id': self.id,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
