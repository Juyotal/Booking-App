import re
import uuid

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from marshmallow import Schema, fields, validates, ValidationError


db = SQLAlchemy()

class RoomBooking(db.Model):
    """Room booking model for conference facilities."""
    __tablename__ = 'room_bookings'

    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.String(36), nullable=False)  # UUID as string
    booked_by = db.Column(db.String(100), nullable=False)
    booking_start = db.Column(db.DateTime, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now())
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(), onupdate=lambda: datetime.now())

    @property
    def booking_end(self):
        """Calculate the booking end time based on start time and duration."""
        if self.booking_start and self.duration_minutes:
            return self.booking_start + timedelta(minutes=self.duration_minutes)
        return None

    def __repr__(self):
        return f'<RoomBooking {self.id}: {self.room_id} booked by {self.booked_by}>'
    

class FormattedDateTimeField(fields.DateTime):
    """Custom field to format datetime as 'January 5th 2025 12:55'"""
    FORMAT = "%B %d %Y %H:%M"
    
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        
        if isinstance(value, str):
            value = datetime.fromisoformat(value.replace('Z', '+00:00'))
            
        return value.strftime(self.FORMAT)
    
    def _deserialize(self, value, attr, data, **kwargs):
        if value is None:
            return None
        
        try:
            if isinstance(value, str):
                try:
                    return datetime.strptime(value, self.FORMAT)
                except ValueError:
                    try:
                        return datetime.fromisoformat(value.replace('Z', '+00:00'))
                    except ValueError:
                        raise ValidationError(f"Invalid date format. Expected either format: {self.FORMAT} or ISO format")
            elif isinstance(value, datetime):
                return value
        except ValueError:
            raise ValidationError(f"Invalid date format. Expected format: {self.FORMAT}")
        
        return value
        

class RoomBookingSchema(Schema):
    """Schema for serializing/deserializing room bookings."""
    id = fields.Integer(dump_only=True)
    room_id = fields.String(required=True)
    booked_by = fields.String(required=True)
    booking_start = FormattedDateTimeField(required=True)
    duration_minutes = fields.Integer(required=True)
    booking_end = FormattedDateTimeField(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @validates('room_id')
    def validate_room_id(self, value):
        """Validate that room_id is a valid UUID."""
        uuid_pattern = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', re.IGNORECASE)
        if not uuid_pattern.match(value):
            raise ValidationError('Invalid UUID format for room_id')
        return value

    @validates('booked_by')
    def validate_booked_by(self, value):
        """Validate that booked_by is not empty and has a reasonable length."""
        if not value.strip():
            raise ValidationError('Booked by cannot be empty')
        if len(value) > 100:
            raise ValidationError('Booked by name is too long (max 100 characters)')
        return value

    @validates('duration_minutes')
    def validate_duration(self, value):
        """Validate that duration is positive and reasonable."""
        if value <= 0:
            raise ValidationError('Duration must be positive')
        if value > 24 * 60:  # 24 hours in minutes
            raise ValidationError('Duration cannot exceed 24 hours')
        return value

    @validates('booking_start')
    def validate_booking_start(self, value):
        """Validate that booking_start is not in the past."""
        if isinstance(value, datetime) and value < datetime.now():
            raise ValidationError('Booking start time cannot be in the past')
        return value

