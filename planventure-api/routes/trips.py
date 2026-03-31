"""
Trip management routes for CRUD operations
"""
from flask import Blueprint, request, jsonify
from datetime import datetime
from database import db
from models.trip import Trip
from models.user import User
from auth_middleware import protected_route, get_current_user_id
from schemas import trip_schema, trips_schema, trip_create_schema
from marshmallow import ValidationError

trips_bp = Blueprint('trips', __name__, url_prefix='/api/trips')


def validate_date_range(start_date, end_date):
    """
    Validate that start_date is before end_date.
    
    Args:
        start_date: Start datetime
        end_date: End datetime
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if start_date >= end_date:
        return False, "Start date must be before end date"
    return True, ""


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


@trips_bp.route('', methods=['POST'])
@protected_route
def create_trip():
    """
    Create a new trip for the authenticated user.
    
    Request body (JSON):
    {
        "destination": "Paris, France",
        "start_date": "2026-06-01T00:00:00",
        "end_date": "2026-06-15T00:00:00",
        "latitude": 48.8566,
        "longitude": 2.3522,
        "description": "Summer vacation in Paris"
    }
    
    Returns:
    {
        "message": "Trip created successfully",
        "data": {
            "id": 1,
            "destination": "Paris, France",
            "start_date": "2026-06-01T00:00:00",
            "end_date": "2026-06-15T00:00:00",
            ...
        }
    }
    
    Status codes:
    - 201: Trip created successfully
    - 400: Invalid input or validation error
    - 401: Unauthorized
    - 500: Server error
    """
    try:
        user_id = get_current_user_id()
        
        # Validate user_id
        if not user_id:
            return jsonify({
                'error': 'auth_error',
                'message': 'User ID not found in authentication token'
            }), 401
        
        # Ensure user_id is an integer
        user_id = int(user_id)
        
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'validation_error',
                'message': 'Request body must be valid JSON'
            }), 400
        
        # Validate input schema
        try:
            validated_data = trip_create_schema.load(data)
        except ValidationError as err:
            return jsonify({
                'error': 'validation_error',
                'message': 'Invalid input data',
                'errors': err.messages
            }), 400
        
        # Validate date range
        start_date = validated_data.get('start_date')
        end_date = validated_data.get('end_date')
        
        is_valid, error_msg = validate_date_range(start_date, end_date)
        if not is_valid:
            return jsonify({
                'error': 'validation_error',
                'message': error_msg
            }), 400
        
        # Create trip object
        trip = Trip(
            user_id=user_id,
            destination=validated_data['destination'],
            start_date=start_date,
            end_date=end_date,
            latitude=validated_data.get('latitude'),
            longitude=validated_data.get('longitude'),
            description=validated_data.get('description', '')
        )
        
        # Add to session
        db.session.add(trip)
        
        # Commit the transaction
        db.session.commit()
        
        # Refresh the object to ensure all fields are populated (including auto-generated ID)
        db.session.refresh(trip)
        
        # Return the created trip
        return jsonify({
            'message': 'Trip created successfully',
            'data': trip.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        import logging
        logging.error(f"Error creating trip: {str(e)}", exc_info=True)
        return jsonify({
            'error': 'server_error',
            'message': 'An error occurred while creating the trip',
            'debug': str(e) if True else None  # Remove in production
        }), 500


@trips_bp.route('', methods=['GET'])
@protected_route
def get_all_trips():
    """
    Get all trips for the authenticated user.
    
    Query parameters:
    - limit: Maximum number of trips to return (default: 50, max: 1000)
    - offset: Number of trips to skip (default: 0)
    
    Returns:
    {
        "message": "Trips retrieved successfully",
        "data": [
            {
                "id": 1,
                "destination": "Paris, France",
                "start_date": "2026-06-01T00:00:00",
                ...
            }
        ],
        "pagination": {
            "total": 5,
            "limit": 50,
            "offset": 0
        }
    }
    
    Status codes:
    - 200: Success
    - 401: Unauthorized
    - 500: Server error
    """
    try:
        user_id = get_current_user_id()
        
        # Get pagination parameters
        limit = min(int(request.args.get('limit', 50)), 1000)
        offset = int(request.args.get('offset', 0))
        
        # Query trips for user
        query = Trip.query.filter_by(user_id=user_id).order_by(Trip.start_date.desc())
        total = query.count()
        
        trips = query.limit(limit).offset(offset).all()
        
        return jsonify({
            'message': 'Trips retrieved successfully',
            'data': [trip.to_dict() for trip in trips],
            'pagination': {
                'total': total,
                'limit': limit,
                'offset': offset
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            'error': 'server_error',
            'message': 'An error occurred while retrieving trips'
        }), 500


@trips_bp.route('/<int:trip_id>', methods=['GET'])
@protected_route
def get_trip(trip_id):
    """
    Get a specific trip by ID (only if user owns it).
    
    Returns:
    {
        "message": "Trip retrieved successfully",
        "data": {
            "id": 1,
            "destination": "Paris, France",
            "start_date": "2026-06-01T00:00:00",
            ...
        }
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
        
        trip = Trip.query.get(trip_id)
        
        if not trip:
            return jsonify({
                'error': 'not_found',
                'message': 'Trip not found'
            }), 404
        
        # Verify ownership (with debug info)
        print(f"DEBUG: Comparing user_id={user_id} (type: {type(user_id)}) with trip.user_id={trip.user_id} (type: {type(trip.user_id)})")
        if not validate_trip_ownership(trip, user_id):
            return jsonify({
                'error': 'forbidden',
                'message': 'You do not have permission to access this trip',
                'debug': {
                    'current_user_id': user_id,
                    'trip_user_id': trip.user_id,
                    'trip_id': trip_id
                }
            }), 403
        
        return jsonify({
            'message': 'Trip retrieved successfully',
            'data': trip.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({
            'error': 'server_error',
            'message': 'An error occurred while retrieving the trip'
        }), 500


@trips_bp.route('/<int:trip_id>', methods=['PUT'])
@protected_route
def update_trip(trip_id):
    """
    Update a specific trip (only if user owns it).
    
    Request body (JSON) - all fields optional:
    {
        "destination": "Lyon, France",
        "start_date": "2026-07-01T00:00:00",
        "end_date": "2026-07-10T00:00:00",
        "latitude": 45.7640,
        "longitude": 4.8357,
        "description": "Updated trip description"
    }
    
    Returns:
    {
        "message": "Trip updated successfully",
        "data": {
            "id": 1,
            "destination": "Lyon, France",
            ...
        }
    }
    
    Status codes:
    - 200: Update successful
    - 400: Invalid input
    - 401: Unauthorized
    - 403: Forbidden (user doesn't own trip)
    - 404: Trip not found
    - 500: Server error
    """
    try:
        user_id = get_current_user_id()
        
        trip = Trip.query.get(trip_id)
        
        if not trip:
            return jsonify({
                'error': 'not_found',
                'message': 'Trip not found'
            }), 404
        
        # Verify ownership
        if not validate_trip_ownership(trip, user_id):
            return jsonify({
                'error': 'forbidden',
                'message': 'You do not have permission to update this trip'
            }), 403
        
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'validation_error',
                'message': 'Request body must be valid JSON'
            }), 400
        
        # Validate input schema (allow partial updates)
        try:
            validated_data = trip_create_schema.load(data, partial=True)
        except ValidationError as err:
            return jsonify({
                'error': 'validation_error',
                'message': 'Invalid input data',
                'errors': err.messages
            }), 400
        
        # Update fields if provided
        if 'destination' in validated_data:
            trip.destination = validated_data['destination']
        
        if 'start_date' in validated_data:
            trip.start_date = validated_data['start_date']
        
        if 'end_date' in validated_data:
            trip.end_date = validated_data['end_date']
        
        # Validate date range if dates were updated
        if 'start_date' in validated_data or 'end_date' in validated_data:
            is_valid, error_msg = validate_date_range(trip.start_date, trip.end_date)
            if not is_valid:
                db.session.rollback()
                return jsonify({
                    'error': 'validation_error',
                    'message': error_msg
                }), 400
        
        if 'latitude' in validated_data:
            trip.latitude = validated_data['latitude']
        
        if 'longitude' in validated_data:
            trip.longitude = validated_data['longitude']
        
        if 'description' in validated_data:
            trip.description = validated_data['description']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Trip updated successfully',
            'data': trip.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'server_error',
            'message': 'An error occurred while updating the trip'
        }), 500


@trips_bp.route('/<int:trip_id>', methods=['DELETE'])
@protected_route
def delete_trip(trip_id):
    """
    Delete a specific trip (only if user owns it).
    
    Returns:
    {
        "message": "Trip deleted successfully",
        "data": {
            "id": 1,
            "destination": "Paris, France"
        }
    }
    
    Status codes:
    - 200: Delete successful
    - 401: Unauthorized
    - 403: Forbidden (user doesn't own trip)
    - 404: Trip not found
    - 500: Server error
    """
    try:
        user_id = get_current_user_id()
        
        trip = Trip.query.get(trip_id)
        
        if not trip:
            return jsonify({
                'error': 'not_found',
                'message': 'Trip not found'
            }), 404
        
        # Verify ownership
        if not validate_trip_ownership(trip, user_id):
            return jsonify({
                'error': 'forbidden',
                'message': 'You do not have permission to delete this trip'
            }), 403
        
        # Store trip info before deletion for response
        trip_data = trip.to_dict()
        
        db.session.delete(trip)
        db.session.commit()
        
        return jsonify({
            'message': 'Trip deleted successfully',
            'data': {
                'id': trip_data['id'],
                'destination': trip_data['destination']
            }
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'server_error',
            'message': 'An error occurred while deleting the trip'
        }), 500


@trips_bp.route('/<int:trip_id>/stats', methods=['GET'])
@protected_route
def get_trip_stats(trip_id):
    """
    Get statistics for a specific trip.
    
    Returns:
    {
        "message": "Trip statistics retrieved successfully",
        "data": {
            "trip_id": 1,
            "destination": "Paris, France",
            "total_days": 14,
            "total_activities": 8,
            "duration_days": 14
        }
    }
    
    Status codes:
    - 200: Success
    - 401: Unauthorized
    - 403: Forbidden
    - 404: Trip not found
    - 500: Server error
    """
    try:
        user_id = get_current_user_id()
        
        trip = Trip.query.get(trip_id)
        
        if not trip:
            return jsonify({
                'error': 'not_found',
                'message': 'Trip not found'
            }), 404
        
        # Verify ownership
        if not validate_trip_ownership(trip, user_id):
            return jsonify({
                'error': 'forbidden',
                'message': 'You do not have permission to access this trip'
            }), 403
        
        # Calculate statistics
        duration = (trip.end_date - trip.start_date).days
        total_activities = len(trip.itinerary_items)
        
        return jsonify({
            'message': 'Trip statistics retrieved successfully',
            'data': {
                'trip_id': trip.id,
                'destination': trip.destination,
                'total_days': duration,
                'total_activities': total_activities,
                'start_date': trip.start_date.isoformat(),
                'end_date': trip.end_date.isoformat()
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            'error': 'server_error',
            'message': 'An error occurred while retrieving trip statistics'
        }), 500
