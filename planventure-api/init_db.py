"""
Database initialization script

This script initializes the database by creating all tables defined in the models.
Run this script to set up the database:
    python init_db.py
"""
from app import app, db


def init_database():
    """Initialize the database by creating all tables"""
    with app.app_context():
        print("Initializing database...")
        db.create_all()
        print("[OK] Database tables created successfully!")
        print("\nTables created:")
        print("  - users")
        print("  - trips")
        print("  - itinerary_items")
        print("\nDatabase initialized at:", app.config['SQLALCHEMY_DATABASE_URI'])


if __name__ == '__main__':
    init_database()
