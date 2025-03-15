import uuid
from datetime import datetime, timedelta
from app import create_app
from app.models import db, RoomBooking

def generate_sample_data():
    """Generate sample room booking data."""
    app = create_app()
    with app.app_context():
        db.session.query(RoomBooking).delete()
        db.session.commit()
        
        room_ids = [str(uuid.uuid4()) for _ in range(3)]
        
        now = datetime.now()
        
        bookings = [
            # Room 1 bookings
            RoomBooking(
                room_id=room_ids[0],
                booked_by="John Doe",
                booking_start=now + timedelta(days=1, hours=9),
                duration_minutes=60
            ),
            RoomBooking(
                room_id=room_ids[0],
                booked_by="Jane Smith",
                booking_start=now + timedelta(days=1, hours=13),
                duration_minutes=90
            ),
            
            # Room 2 bookings
            RoomBooking(
                room_id=room_ids[1],
                booked_by="Alice Johnson",
                booking_start=now + timedelta(days=2, hours=10),
                duration_minutes=120
            ),
            
            # Room 3 bookings
            RoomBooking(
                room_id=room_ids[2],
                booked_by="Bob Brown",
                booking_start=now + timedelta(days=3, hours=14),
                duration_minutes=45
            ),
            RoomBooking(
                room_id=room_ids[2],
                booked_by="Charlie Wilson",
                booking_start=now + timedelta(days=3, hours=16),
                duration_minutes=30
            )
        ]
        
        # Add to database
        for booking in bookings:
            db.session.add(booking)
        
        db.session.commit()
        
        print(f"Added {len(bookings)} sample bookings for {len(room_ids)} rooms.")
        
        # Print the created bookings
        for booking in RoomBooking.query.all():
            print(f"Booking {booking.id}: Room {booking.room_id} booked by {booking.booked_by} "
                  f"from {booking.booking_start} for {booking.duration_minutes} minutes "
                  f"(ends at {booking.booking_end})")

if __name__ == '__main__':
    generate_sample_data() 