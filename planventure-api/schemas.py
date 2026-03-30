"""
Marshmallow schemas for data validation and serialization
"""
from marshmallow import Schema, fields, validate, ValidationError
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.user import User
from models.trip import Trip
from models.itinerary_item import ItineraryItem


class UserSchema(SQLAlchemyAutoSchema):
    """Schema for User model with validation"""
    class Meta:
        model = User
        load_instance = True
        dump_only = ('id', 'created_at', 'updated_at')

    email = fields.Email(required=True, validate=validate.Length(min=5, max=255))
    password = fields.String(required=True, load_only=True, validate=validate.Length(min=8))
    password_hash = fields.String(dump_only=True)


class UserRegisterSchema(Schema):
    """Schema for user registration"""
    email = fields.Email(required=True, validate=validate.Length(min=5, max=255))
    password = fields.String(required=True, validate=validate.Length(min=8, error="Password must be at least 8 characters"))


class UserLoginSchema(Schema):
    """Schema for user login"""
    email = fields.Email(required=True)
    password = fields.String(required=True)


class ItineraryItemSchema(SQLAlchemyAutoSchema):
    """Schema for ItineraryItem model"""
    class Meta:
        model = ItineraryItem
        load_instance = True
        dump_only = ('id', 'trip_id', 'created_at', 'updated_at')

    day = fields.Integer(required=True, validate=validate.Range(min=1))
    title = fields.String(required=True, validate=validate.Length(min=1, max=255))
    description = fields.String(required=False)
    activity_date = fields.DateTime(required=True)
    latitude = fields.Float(required=False)
    longitude = fields.Float(required=False)
    location = fields.String(required=False, validate=validate.Length(max=255))


class TripSchema(SQLAlchemyAutoSchema):
    """Schema for Trip model with validation"""
    class Meta:
        model = Trip
        load_instance = True
        dump_only = ('id', 'user_id', 'created_at', 'updated_at')

    destination = fields.String(required=True, validate=validate.Length(min=1, max=255))
    start_date = fields.DateTime(required=True)
    end_date = fields.DateTime(required=True)
    latitude = fields.Float(required=False)
    longitude = fields.Float(required=False)
    description = fields.String(required=False)
    itinerary_items = fields.Nested(ItineraryItemSchema, many=True, dump_only=True)


class TripCreateSchema(Schema):
    """Schema for creating a new trip"""
    destination = fields.String(required=True, validate=validate.Length(min=1, max=255))
    start_date = fields.DateTime(required=True)
    end_date = fields.DateTime(required=True)
    latitude = fields.Float(required=False)
    longitude = fields.Float(required=False)
    description = fields.String(required=False)


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
