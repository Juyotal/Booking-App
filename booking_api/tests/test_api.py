import unittest
import json
from datetime import datetime, timedelta
import uuid

from app import create_app
from app.models import db, RoomBooking

class RoomBookingAPITestCase(unittest.TestCase):
    """Test case for the room booking API."""

    def setUp(self):
        """Set up test client and database."""
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
        # Sample valid booking data
        self.valid_booking = {
            'room_id': str(uuid.uuid4()),
            'booked_by': 'Test User',
            'booking_start': (datetime.now() + timedelta(hours=1)).isoformat(),
            'duration_minutes': 60
        }

    def tearDown(self):
        """Clean up after tests."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_booking(self):
        """Test creating a new booking."""
        response = self.client.post(
            '/api/bookings',
            data=json.dumps(self.valid_booking),
            content_type='application/json'
        )
        print(response.data)
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['booked_by'], 'Test User')
        self.assertEqual(data['duration_minutes'], 60)
        self.assertIn('booking_end', data)

    def test_create_booking_invalid_data(self):
        """Test creating a booking with invalid data."""
        # Missing required field
        invalid_booking = self.valid_booking.copy()
        del invalid_booking['booked_by']
        
        response = self.client.post(
            '/api/bookings',
            data=json.dumps(invalid_booking),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        
        invalid_booking = self.valid_booking.copy()
        invalid_booking['room_id'] = 'not-a-uuid'
        
        response = self.client.post(
            '/api/bookings',
            data=json.dumps(invalid_booking),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        
        invalid_booking = self.valid_booking.copy()
        invalid_booking['duration_minutes'] = -10
        
        response = self.client.post(
            '/api/bookings',
            data=json.dumps(invalid_booking),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)

    def test_get_bookings(self):
        """Test getting all bookings."""
        self.client.post(
            '/api/bookings',
            data=json.dumps(self.valid_booking),
            content_type='application/json'
        )
        
        response = self.client.get('/api/bookings')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['booked_by'], 'Test User')

    def test_get_booking(self):
        """Test getting a specific booking."""
        create_response = self.client.post(
            '/api/bookings',
            data=json.dumps(self.valid_booking),
            content_type='application/json'
        )
        booking_id = json.loads(create_response.data)['id']
        
        response = self.client.get(f'/api/bookings/{booking_id}')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['id'], booking_id)
        self.assertEqual(data['booked_by'], 'Test User')
        self.assertIn('booking_end', data)

    def test_get_nonexistent_booking(self):
        """Test getting a booking that doesn't exist."""
        response = self.client.get('/api/bookings/999')
        self.assertEqual(response.status_code, 404)

    def test_update_booking(self):
        """Test updating a booking."""
        create_response = self.client.post(
            '/api/bookings',
            data=json.dumps(self.valid_booking),
            content_type='application/json'
        )
        booking_id = json.loads(create_response.data)['id']
        
        update_data = self.valid_booking.copy()
        update_data['booked_by'] = 'Updated User'
        update_data['duration_minutes'] = 90
        
        response = self.client.put(
            f'/api/bookings/{booking_id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['id'], booking_id)
        self.assertEqual(data['booked_by'], 'Updated User')
        self.assertEqual(data['duration_minutes'], 90)

    def test_delete_booking(self):
        """Test deleting a booking."""
        create_response = self.client.post(
            '/api/bookings',
            data=json.dumps(self.valid_booking),
            content_type='application/json'
        )
        booking_id = json.loads(create_response.data)['id']
        
        response = self.client.delete(f'/api/bookings/{booking_id}')
        self.assertEqual(response.status_code, 204)
        
        get_response = self.client.get(f'/api/bookings/{booking_id}')
        self.assertEqual(get_response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
