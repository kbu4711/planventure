"""
Itinerary item management routes for CRUD operations
"""
from flask import Blueprint, request, jsonify
from datetime import datetime
from database import db
from models.trip import Trip
from models.itinerary_item import ItineraryItem
from auth_middleware import protected_route, get_current_user_id
from schemas import itinerary_item_schema, itinerary_items_schema
from marshmallow import ValidationError

itinerary_bp = Blueprint('itinerary', __name__, url_prefix='/api/trips')


def validate_trip_ownership(trip, user_id):
    """
    Validate that trip belongs to the authenticated user.
    
    Args:
        trip: Trip object
        user_id: Current user ID
        
    Returns:
        True if user owns trip, False otherwise
    """
    return trip.user_id == user_id


@itinerary_bp.route('/<int:trip_id>/itinerary/items', methods=['GET'])
@protected_route
def get_itinerary_items(trip_id):
    """
    Get all itinerary items for a specific trip.
    
    Query parameters:
    - day: Filter by day number (optional)
    
    Returns:
    {
        "message": "Itinerary items retrieved successfully",
        "data": [
            {
                "id": 1,
                "trip_id": 1,
                "day": 1,
                "title": "Day 1 - Paris, France",
                "activities": [...],
                ...
            }
        ]
    }
    
    Status codes:
    - 200: Success
    - 401: Unauthorized
    - 403: Forbidden (user doesn't own trip)
    - 404: Trip not found
    - 500: Server error
    """
    try:
        user_id = get_current_user_id()
        
        # Get and verify trip ownership
        trip = Trip.query.get(trip_id)
        if not trip:
            return jsonify({
                'error': 'not_found',
                'message': 'Trip not found'
            }), 404
        
        if not validate_trip_ownership(trip, user_id):
            return jsonify({
                'error': 'forbidden',
                'message': 'You do not have permission to access this trip'
            }), 403
        
        # Filter by day if provided
        query = ItineraryItem.query.filter_by(trip_id=trip_id)
        day = request.args.get('day', type=int)
        if day:
            query = query.filter_by(day=day)
        
        items = query.order_by(ItineraryItem.day).all()
        
        return jsonify({
            'message': 'Itinerary items retrieved successfully',
            'data': [item.to_dict() for item in items]
        }), 200
    
    except Exception as e:
        return jsonify({
            'error': 'server_error',
            'message': 'An error occurred while retrieving itinerary items'
        }), 500


@itinerary_bp.route('/<int:trip_id>/itinerary/items/<int:item_id>', methods=['GET'])
@protected_route
def get_itinerary_item(trip_id, item_id):
    """
    Get a specific itinerary item by ID.
    
    Returns:
    {
        "message": "Itinerary item retrieved successfully",
        "data": {
            "id": 1,
            "trip_id": 1,
            "day": 1,
            "title": "Day 1 - Paris, France",
            ...
        }
    }
    
    Status codes:
    - 200: Success
    - 401: Unauthorized
    - 403: Forbidden
    - 404: Not found
    - 500: Server error
    """
    try:
        user_id = get_current_user_id()
        
        # Verify trip ownership
        trip = Trip.query.get(trip_id)
        if not trip:
            return jsonify({
                'error': 'not_found',
                'message': 'Trip not found'
            }), 404
        
        if not validate_trip_ownership(trip, user_id):
            return jsonify({
                'error': 'forbidden',
                'message': 'You do not have permission to access this trip'
            }), 403
        
        # Get the itinerary item
        item = ItineraryItem.query.filter_by(id=item_id, trip_id=trip_id).first()
        if not item:
            return jsonify({
                'error': 'not_found',
                'message': 'Itinerary item not found'
            }), 404
        
        return jsonify({
            'message': 'Itinerary item retrieved successfully',
            'data': item.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({
            'error': 'server_error',
            'message': 'An error occurred while retrieving the itinerary item'
        }), 500


@itinerary_bp.route('/<int:trip_id>/itinerary/items', methods=['POST'])
@protected_route
def create_itinerary_item(trip_id):
    """
    Create a new itinerary item for a trip.
    
    Request body (JSON):
    {
        "day": 1,
        "title": "Day 1 Exploration",
        "description": "Explore the city",
        "activity_date": "2026-06-01T09:00:00",
        "location": "Paris, France",
        "latitude": 48.8566,
        "longitude": 2.3522,
        "breakfast_time": "08:00:00",
        "lunch_time": "12:00:00",
        "dinner_time": "19:00:00",
        "accommodation_name": "Hotel de la Paix",
        "accommodation_address": "123 Rue de la Paix, Paris",
        "activities": [
            {
                "name": "Visit Eiffel Tower",
                "time": "10:00",
                "duration_minutes": 120,
                "location": "Eiffel Tower",
                "notes": "Book tickets in advance"
            }
        ]
    }
    
    Returns:
    {
        "message": "Itinerary item created successfully",
        "data": { ... }
    }
    
    Status codes:
    - 201: Created
    - 400: Invalid input
    - 401: Unauthorized
    - 403: Forbidden
    - 404: Trip not found
    - 500: Server error
    """
    try:
        user_id = get_current_user_id()
        
        # Verify trip ownership
        trip = Trip.query.get(trip_id)
        if not trip:
            return jsonify({
                'error': 'not_found',
                'message': 'Trip not found'
            }), 404
        
        if not validate_trip_ownership(trip, user_id):
            return jsonify({
                'error': 'forbidden',
                'message': 'You do not have permission to modify this trip'
            }), 403
        
        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'validation_error',
                'message': 'Request body must be valid JSON'
            }), 400
        
        # Validate input schema
        try:
            validated_data = itinerary_item_schema.load(data)
        except ValidationError as err:
            return jsonify({
                'error': 'validation_error',
                'message': 'Invalid input data',
                'errors': err.messages
            }), 400
        
        # Create itinerary item
        item = ItineraryItem(
            trip_id=trip_id,
            day=validated_data['day'],
            title=validated_data['title'],
            description=validated_data.get('description'),
            activity_date=validated_data['activity_date'],
            latitude=validated_data.get('latitude'),
            longitude=validated_data.get('longitude'),
            location=validated_data.get('location'),
            breakfast_time=validated_data.get('breakfast_time'),
            lunch_time=validated_data.get('lunch_time'),
            dinner_time=validated_data.get('dinner_time'),
            accommodation_name=validated_data.get('accommodation_name'),
            accommodation_address=validated_data.get('accommodation_address'),
            activities=validated_data.get('activities', [])
        )
        
        db.session.add(item)
        db.session.commit()
        
        return jsonify({
            'message': 'Itinerary item created successfully',
            'data': item.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        import logging
        logging.error(f"Error creating itinerary item: {str(e)}", exc_info=True)
        return jsonify({
            'error': 'server_error',
            'message': 'An error occurred while creating the itinerary item'
        }), 500


@itinerary_bp.route('/<int:trip_id>/itinerary/items/<int:item_id>', methods=['PUT'])
@protected_route
def update_itinerary_item(trip_id, item_id):
    """
    Update an existing itinerary item.
    
    Request body (JSON):
    {
        "day": 1,
        "title": "Updated Day 1",
        "description": "Updated description",
        "activity_date": "2026-06-01T09:00:00",
        "location": "Paris, France",
        "latitude": 48.8566,
        "longitude": 2.3522,
        "breakfast_time": "08:00:00",
        "lunch_time": "12:00:00",
        "dinner_time": "19:00:00",
        "accommodation_name": "Hotel de la Paix",
        "accommodation_address": "123 Rue de la Paix, Paris",
        "activities": [...]
    }
    
    Returns:
    {
        "message": "Itinerary item updated successfully",
        "data": { ... }
    }
    
    Status codes:
    - 200: Updated
    - 400: Invalid input
    - 401: Unauthorized
    - 403: Forbidden
    - 404: Not found
    - 500: Server error
    """
    try:
        user_id = get_current_user_id()
        
        # Verify trip ownership
        trip = Trip.query.get(trip_id)
        if not trip:
            return jsonify({
                'error': 'not_found',
                'message': 'Trip not found'
            }), 404
        
        if not validate_trip_ownership(trip, user_id):
            return jsonify({
                'error': 'forbidden',
                'message': 'You do not have permission to modify this trip'
            }), 403
        
        # Get the itinerary item
        item = ItineraryItem.query.filter_by(id=item_id, trip_id=trip_id).first()
        if not item:
            return jsonify({
                'error': 'not_found',
                'message': 'Itinerary item not found'
            }), 404
        
        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'validation_error',
                'message': 'Request body must be valid JSON'
            }), 400
        
        # Validate input schema
        try:
            validated_data = itinerary_item_schema.load(data)
        except ValidationError as err:
            return jsonify({
                'error': 'validation_error',
                'message': 'Invalid input data',
                'errors': err.messages
            }), 400
        
        # Update itinerary item
        item.day = validated_data['day']
        item.title = validated_data['title']
        item.description = validated_data.get('description')
        item.activity_date = validated_data['activity_date']
        item.latitude = validated_data.get('latitude')
        item.longitude = validated_data.get('longitude')
        item.location = validated_data.get('location')
        item.breakfast_time = validated_data.get('breakfast_time')
        item.lunch_time = validated_data.get('lunch_time')
        item.dinner_time = validated_data.get('dinner_time')
        item.accommodation_name = validated_data.get('accommodation_name')
        item.accommodation_address = validated_data.get('accommodation_address')
        item.activities = validated_data.get('activities', [])
        
        db.session.commit()
        
        return jsonify({
            'message': 'Itinerary item updated successfully',
            'data': item.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        import logging
        logging.error(f"Error updating itinerary item: {str(e)}", exc_info=True)
        return jsonify({
            'error': 'server_error',
            'message': 'An error occurred while updating the itinerary item'
        }), 500


@itinerary_bp.route('/<int:trip_id>/itinerary/items/<int:item_id>', methods=['DELETE'])
@protected_route
def delete_itinerary_item(trip_id, item_id):
    """
    Delete an itinerary item.
    
    Returns:
    {
        "message": "Itinerary item deleted successfully"
    }
    
    Status codes:
    - 200: Deleted
    - 401: Unauthorized
    - 403: Forbidden
    - 404: Not found
    - 500: Server error
    """
    try:
        user_id = get_current_user_id()
        
        # Verify trip ownership
        trip = Trip.query.get(trip_id)
        if not trip:
            return jsonify({
                'error': 'not_found',
                'message': 'Trip not found'
            }), 404
        
        if not validate_trip_ownership(trip, user_id):
            return jsonify({
                'error': 'forbidden',
                'message': 'You do not have permission to modify this trip'
            }), 403
        
        # Get and delete the itinerary item
        item = ItineraryItem.query.filter_by(id=item_id, trip_id=trip_id).first()
        if not item:
            return jsonify({
                'error': 'not_found',
                'message': 'Itinerary item not found'
            }), 404
        
        db.session.delete(item)
        db.session.commit()
        
        return jsonify({
            'message': 'Itinerary item deleted successfully'
        }), 200
    
    except Exception as e:
        db.session.rollback()
        import logging
        logging.error(f"Error deleting itinerary item: {str(e)}", exc_info=True)
        return jsonify({
            'error': 'server_error',
            'message': 'An error occurred while deleting the itinerary item'
        }), 500
