"""
ItineraryItem model for individual activities/events within a trip
"""
from datetime import datetime, timezone
from database import db


class ItineraryItem(db.Model):
    """ItineraryItem model for individual activities/events within a trip"""
    __tablename__ = 'itinerary_items'

    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=False, index=True)
    day = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    activity_date = db.Column(db.DateTime, nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    location = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    def __repr__(self):
        return f'<ItineraryItem Day {self.day}: {self.title}>'

    def to_dict(self):
        """Convert itinerary item to dictionary representation"""
        return {
            'id': self.id,
            'trip_id': self.trip_id,
            'day': self.day,
            'title': self.title,
            'description': self.description,
            'activity_date': self.activity_date.isoformat(),
            'latitude': self.latitude,
            'longitude': self.longitude,
            'location': self.location,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
