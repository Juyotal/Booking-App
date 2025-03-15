from flask import Blueprint, request, jsonify, render_template
from marshmallow import ValidationError

from .models import db, RoomBooking, RoomBookingSchema

# Create a blueprint for the API
api = Blueprint('api', __name__, template_folder='templates')
booking_schema = RoomBookingSchema()
bookings_schema = RoomBookingSchema(many=True)

@api.route('/api/docs', methods=['GET'])
def api_docs():
    """Render API documentation."""
    return render_template('api_docs.html')

@api.route('/api/bookings', methods=['POST'])
def create_booking():
    """Create a new room booking."""
    try:
        booking_data = booking_schema.load(request.json)
        
        booking = RoomBooking(
            room_id=booking_data['room_id'],
            booked_by=booking_data['booked_by'],
            booking_start=booking_data['booking_start'],
            duration_minutes=booking_data['duration_minutes']
        )
        
        db.session.add(booking)
        db.session.commit()
        
        result = booking_schema.dump(booking)
        
        return jsonify(result), 201
        
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@api.route('/api/bookings', methods=['GET'])
def get_bookings():
    """Get all room bookings."""
    bookings = RoomBooking.query.all()
    result = bookings_schema.dump(bookings)
    
    return jsonify(result), 200

@api.route('/api/bookings/<int:id>', methods=['GET'])
def get_booking(id):
    """Get a specific room booking by ID."""
    booking = RoomBooking.query.get(id)
    
    if not booking:
        return jsonify({"message": "Booking not found"}), 404
    
    result = booking_schema.dump(booking)
    
    return jsonify(result), 200

@api.route('/api/bookings/<int:id>', methods=['PUT'])
def update_booking(id):
    """Update an existing room booking."""
    booking = RoomBooking.query.get(id)
    
    if not booking:
        return jsonify({"message": "Booking not found"}), 404
    
    try:
        booking_data = booking_schema.load(request.json)
        
        booking.room_id = booking_data['room_id']
        booking.booked_by = booking_data['booked_by']
        booking.booking_start = booking_data['booking_start']
        booking.duration_minutes = booking_data['duration_minutes']
        
        db.session.commit()
        
        result = booking_schema.dump(booking)
        
        return jsonify(result), 200
        
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@api.route('/api/bookings/<int:id>', methods=['DELETE'])
def delete_booking(id):
    """Delete a room booking."""
    booking = RoomBooking.query.get(id)
    
    if not booking:
        return jsonify({"message": "Booking not found"}), 404
    
    try:
        db.session.delete(booking)
        db.session.commit()
        return "", 204
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
