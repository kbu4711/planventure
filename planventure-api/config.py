"""
Configuration settings for PlanVenture API

This module manages all application configuration based on the environment.
Configuration is loaded from environment variables with sensible defaults.

Usage:
    from config import config
    app.config.from_object(config)
"""

import os
from datetime import timedelta


class Config:
    """Base configuration class with common settings"""
    
    # Flask Configuration
    JSON_SORT_KEYS = False
    PROPAGATE_EXCEPTIONS = True
    
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///planventure.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 3600,
        'pool_pre_ping': True,
    }
    
    # JWT Configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=int(os.getenv('ACCESS_TOKEN_EXPIRES', 3600)))
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(seconds=int(os.getenv('REFRESH_TOKEN_EXPIRES', 604800)))
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'
    
    # CORS Configuration
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://localhost:5173')
    CORS_METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'PATCH']
    CORS_ALLOW_HEADERS = ['Content-Type', 'Authorization', 'X-Requested-With']
    CORS_EXPOSE_HEADERS = ['Content-Type', 'X-Total-Count', 'X-Page-Count']
    CORS_SUPPORTS_CREDENTIALS = True
    CORS_MAX_AGE = 3600
    CORS_SEND_WILDCARD = False
    
    @staticmethod
    def get_cors_origins():
        """
        Parse and return CORS origins as a list.
        
        Returns:
            list: List of allowed CORS origins with whitespace stripped
        """
        origins = Config.CORS_ORIGINS.split(',')
        return [origin.strip() for origin in origins]


class DevelopmentConfig(Config):
    """Development environment configuration"""
    
    DEBUG = True
    TESTING = False
    
    # SQLAlchemy verbose logging
    SQLALCHEMY_ECHO = os.getenv('SQL_ECHO', 'False').lower() == 'true'
    
    # Development CORS origins
    CORS_ORIGINS = os.getenv(
        'CORS_ORIGINS',
        'http://localhost:3000,http://localhost:5173,http://127.0.0.1:3000,http://127.0.0.1:5173'
    )


class TestingConfig(Config):
    """Testing environment configuration"""
    
    DEBUG = False
    TESTING = True
    
    # Use in-memory SQLite for testing
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    
    # Disable CSRF for testing
    WTF_CSRF_ENABLED = False
    
    # Testing CORS is more permissive
    CORS_ORIGINS = 'http://localhost:3000,http://localhost:5173'
    
    # Shorter token expiry for testing
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=300)


class ProductionConfig(Config):
    """Production environment configuration"""
    
    DEBUG = False
    TESTING = False
    
    # SQLAlchemy silent by default
    SQLALCHEMY_ECHO = False
    
    # Stricter CORS in production - requires environment variable
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '')
    
    # Validate production configuration
    @classmethod
    def validate(cls):
        """
        Validate production configuration.
        
        Raises:
            ValueError: If critical production settings are missing or invalid
        """
        if not cls.JWT_SECRET_KEY or cls.JWT_SECRET_KEY == 'dev-secret-key-change-in-production':
            raise ValueError('JWT_SECRET_KEY must be set in production')
        
        if not cls.CORS_ORIGINS:
            raise ValueError('CORS_ORIGINS must be set in production')
        
        if 'localhost' in cls.CORS_ORIGINS or '127.0.0.1' in cls.CORS_ORIGINS:
            raise ValueError('Production CORS_ORIGINS cannot contain localhost')
        
        return True


# Configuration dictionary for easy access
config_by_env = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}


def get_config():
    """
    Get the appropriate configuration based on the Flask environment.
    
    Returns:
        Config: The configuration class for the current environment
        
    Raises:
        ValueError: If environment is not recognized
    """
    env = os.getenv('FLASK_ENV', 'development').lower()
    
    if env not in config_by_env:
        raise ValueError(f"Unknown environment: {env}. Must be one of {list(config_by_env.keys())}")
    
    config_class = config_by_env[env]
    
    # Validate production config before returning
    if env == 'production':
        config_class.validate()
    
    return config_class


# Default export for current environment
config = get_config()
