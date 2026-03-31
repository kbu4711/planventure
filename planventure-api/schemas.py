"""
Marshmallow schemas for data validation and serialization
"""
from marshmallow import Schema, fields, validate, ValidationError


class UserRegisterSchema(Schema):
    """Schema for user registration"""
    email = fields.Email(required=True, validate=validate.Length(min=5, max=255))
    password = fields.String(required=True, validate=validate.Length(min=8, error="Password must be at least 8 characters"))


class UserLoginSchema(Schema):
    """Schema for user login"""
    email = fields.Email(required=True)
    password = fields.String(required=True)


class UserSchema(Schema):
    """Schema for User model with validation"""
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True, validate=validate.Length(min=5, max=255))
    password = fields.String(required=True, load_only=True, validate=validate.Length(min=8))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class ItineraryItemSchema(Schema):
    """Schema for ItineraryItem model"""
    id = fields.Int(dump_only=True)
    trip_id = fields.Int(dump_only=True)
    day = fields.Integer(required=True, validate=validate.Range(min=1))
    title = fields.String(required=True, validate=validate.Length(min=1, max=255))
    description = fields.String(required=False)
    activity_date = fields.DateTime(required=True)
    latitude = fields.Float(required=False, allow_none=True)
    longitude = fields.Float(required=False, allow_none=True)
    location = fields.String(required=False, validate=validate.Length(max=255))
    breakfast_time = fields.Time(required=False, allow_none=True)
    lunch_time = fields.Time(required=False, allow_none=True)
    dinner_time = fields.Time(required=False, allow_none=True)
    accommodation_name = fields.String(required=False, validate=validate.Length(max=255))
    accommodation_address = fields.String(required=False)
    activities = fields.List(fields.Dict, required=False)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class TripCreateSchema(Schema):
    """Schema for creating a new trip"""
    destination = fields.String(required=True, validate=validate.Length(min=1, max=255))
    start_date = fields.DateTime(required=True)
    end_date = fields.DateTime(required=True)
    latitude = fields.Float(required=False, allow_none=True)
    longitude = fields.Float(required=False, allow_none=True)
    description = fields.String(required=False)
    itinerary_items = fields.List(fields.Nested(ItineraryItemSchema), required=False)


class TripSchema(Schema):
    """Schema for Trip model with validation"""
    id = fields.Int(dump_only=True)
    user_id = fields.Int(dump_only=True)
    destination = fields.String(required=True, validate=validate.Length(min=1, max=255))
    start_date = fields.DateTime(required=True)
    end_date = fields.DateTime(required=True)
    latitude = fields.Float(required=False, allow_none=True)
    longitude = fields.Float(required=False, allow_none=True)
    description = fields.String(required=False)
    itinerary_items = fields.Nested(ItineraryItemSchema, many=True, dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


# Schema instances
user_schema = UserSchema()
users_schema = UserSchema(many=True)
user_register_schema = UserRegisterSchema()
user_login_schema = UserLoginSchema()

trip_schema = TripSchema()
trips_schema = TripSchema(many=True)
trip_create_schema = TripCreateSchema()

itinerary_item_schema = ItineraryItemSchema()
itinerary_items_schema = ItineraryItemSchema(many=True)
