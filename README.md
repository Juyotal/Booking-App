# Room Booking API

A RESTful API for managing conference room bookings at Bitcube.

## Features

- CRUD operations for room bookings
- Data validation
- PostgreSQL database integration
- Unit tests

## Setup

### Prerequisites

- Python 3.8+
- PostgreSQL

### Installation

1. Clone the repository:
```
git clone <repository-url>
cd Booking-App/booking_api
```

2. Create a virtual environment and activate it:
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory with the following content:
```
DATABASE_URL=postgresql://username:password@localhost/booking_db
FLASK_APP=app
FLASK_ENV=development
```

5. Create the database:
```
createdb booking_db
```

6. Initialize the database:
```
flask db init
flask db migrate
flask db upgrade
```

### To Note: if for some reason you are unable to setup a SQL database to run the project, just set the FLASKENV to "testing" as seen in the example.env

## Running the Application

```
flask run
```

The API will be available at `http://localhost:5000`.

## API Documentation

### Room Booking Endpoints

#### Create a Booking

- **URL**: `/api/bookings`
- **Method**: `POST`
- **Request Body**:
```json
{
  "room_id": "550e8400-e29b-41d4-a716-446655440000",
  "booked_by": "John Doe",
  "booking_start": "January 5th 2025 12:55",
  "duration_minutes": 60
}
```
- **Success Response**:
  - **Code**: 201 Created
  - **Content**:
```json
{
  "id": 1,
  "room_id": "550e8400-e29b-41d4-a716-446655440000",
  "booked_by": "John Doe",
  "booking_start": "2January 5th 2025 12:55",
  "duration_minutes": 60,
  "booking_end": "January 5th 2025 13:55"
}
```

#### Get All Bookings

- **URL**: `/api/bookings`
- **Method**: `GET`
- **Success Response**:
  - **Code**: 200 OK
  - **Content**:
```json
[
  {
    "id": 1,
    "room_id": "550e8400-e29b-41d4-a716-446655440000",
    "booked_by": "John Doe",
    "booking_start": "January 5th 2025 12:55",
    "duration_minutes": 60,
    "booking_end": "January 5th 2025 13:55"
  }
]
```

#### Get a Specific Booking

- **URL**: `/api/bookings/<id>`
- **Method**: `GET`
- **Success Response**:
  - **Code**: 200 OK
  - **Content**:
```json
{
  "id": 1,
  "room_id": "550e8400-e29b-41d4-a716-446655440000",
  "booked_by": "John Doe",
  "booking_start": "January 5th 2025 12:55",
  "duration_minutes": 60,
  "booking_end": "January 5th 2025 13:55"
}
```
- **Error Response**:
  - **Code**: 404 Not Found
  - **Content**: `{"message": "Booking not found"}`

#### Update a Booking

- **URL**: `/api/bookings/<id>`
- **Method**: `PUT`
- **Request Body**:
```json
{
  "room_id": "550e8400-e29b-41d4-a716-446655440000",
  "booked_by": "Jane Smith",
  "booking_start": "January 5th 2025 12:55",
  "duration_minutes": 90
}
```
- **Success Response**:
  - **Code**: 200 OK
  - **Content**:
```json
{
  "id": 1,
  "room_id": "550e8400-e29b-41d4-a716-446655440000",
  "booked_by": "Jane Smith",
  "booking_start": "January 5th 2025 12:55",
  "duration_minutes": 90,
  "booking_end": "January 5th 2025 14:25"
}
```
- **Error Response**:
  - **Code**: 404 Not Found
  - **Content**: `{"message": "Booking not found"}`

#### Delete a Booking

- **URL**: `/api/bookings/<id>`
- **Method**: `DELETE`
- **Success Response**:
  - **Code**: 204 No Content
- **Error Response**:
  - **Code**: 404 Not Found
  - **Content**: `{"message": "Booking not found"}`

## Running Tests

```
pytest
```

## License

MIT
