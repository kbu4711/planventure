"""
Routes package for PlanVenture API
"""
from .auth import auth_bp
from .trips import trips_bp
from .itinerary import itinerary_bp

__all__ = ['auth_bp', 'trips_bp', 'itinerary_bp']
