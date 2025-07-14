# Vehicle Booking API Documentation

## Overview
A comprehensive REST API for managing vehicle bookings, built with Django REST Framework. Supports user authentication, vehicle management, and booking operations.

## Base URL
```
http://127.0.0.1:8000/api/
```

## Authentication
This API uses JWT (JSON Web Tokens) for authentication. Include the access token in the Authorization header for protected endpoints.

```http
Authorization: Bearer <access_token>
```

## Response Format

### Success Response
```json
{
    "message": "Success message",
    "data": { ... }
}
```

### Error Response
```json
{
    "error": "Error message",
    "details": { ... }
}
```

---

## Authentication Endpoints

### Register User
Creates a new user account and returns JWT tokens.

**Endpoint:** `POST /register/`  
**Authentication:** Not required

#### Request Body
```json
{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepassword123",
    "password2": "securepassword123",
    "first_name": "John",
    "last_name": "Doe"
}
```

#### Response (201 Created)
```json
{
    "message": "User registered successfully",
    "user": {
        "id": 1,
        "username": "john_doe",
        "email": "john@example.com",
        "first_name": "John",
        "last_name": "Doe"
    },
    "tokens": {
        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    }
}
```

#### Error Response (400 Bad Request)
```json
{
    "error": "Registration failed",
    "details": {
        "username": ["A user with that username already exists."],
        "password": ["This password is too short."]
    }
}
```

---

### Login User
Authenticates user and returns JWT tokens.

**Endpoint:** `POST /login/`  
**Authentication:** Not required

#### Request Body
```json
{
    "username": "john_doe",
    "password": "securepassword123"
}
```

#### Response (200 OK)
```json
{
    "message": "Login successful",
    "user": {
        "id": 1,
        "username": "john_doe",
        "email": "john@example.com",
        "first_name": "John",
        "last_name": "Doe"
    },
    "tokens": {
        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    }
}
```

#### Error Response (401 Unauthorized)
```json
{
    "error": "Invalid credentials"
}
```

---

### Refresh Token
Refreshes the access token using a valid refresh token.

**Endpoint:** `POST /token/refresh/`  
**Authentication:** Not required

#### Request Body
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### Response (200 OK)
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

---

## User Profile

### Get User Profile
Retrieves the authenticated user's profile information.

**Endpoint:** `GET /profile/`  
**Authentication:** Required

#### Response (200 OK)
```json
{
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "date_joined": "2025-07-11T10:30:00Z"
}
```

---

### Update User Profile
Updates the authenticated user's profile information.

**Endpoint:** `PUT /profile/`  
**Authentication:** Required

#### Request Body
```json
{
    "email": "newemail@example.com",
    "first_name": "Johnny",
    "last_name": "Smith"
}
```

#### Response (200 OK)
```json
{
    "id": 1,
    "username": "john_doe",
    "email": "newemail@example.com",
    "first_name": "Johnny",
    "last_name": "Smith",
    "date_joined": "2025-07-11T10:30:00Z"
}
```

---

## Vehicle Management

### List User Vehicles
Retrieves a paginated list of vehicles owned by the authenticated user.

**Endpoint:** `GET /vehicles/`  
**Authentication:** Required

#### Query Parameters
- `page` (optional): Page number for pagination

#### Response (200 OK)
```json
{
    "count": 25,
    "next": "http://127.0.0.1:8000/api/vehicles/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "make": "Toyota",
            "model": "Camry",
            "year": 2022,
            "license_plate": "ABC-123",
            "color": "Blue",
            "vehicle_type": "sedan",
            "owner": 1,
            "created_at": "2025-07-11T10:30:00Z",
            "updated_at": "2025-07-11T10:30:00Z"
        }
    ]
}
```

---

### Create Vehicle
Adds a new vehicle to the authenticated user's account.

**Endpoint:** `POST /vehicles/`  
**Authentication:** Required

#### Request Body
```json
{
    "make": "Honda",
    "model": "Civic",
    "year": 2023,
    "license_plate": "XYZ-789",
    "color": "Red",
    "vehicle_type": "sedan"
}
```

#### Response (201 Created)
```json
{
    "message": "Vehicle added successfully",
    "vehicle": {
        "id": 2,
        "make": "Honda",
        "model": "Civic",
        "year": 2023,
        "license_plate": "XYZ-789",
        "color": "Red",
        "vehicle_type": "sedan",
        "owner": 1,
        "created_at": "2025-07-11T11:00:00Z",
        "updated_at": "2025-07-11T11:00:00Z"
    }
}
```

#### Error Response (400 Bad Request)
```json
{
    "error": "Failed to add vehicle",
    "details": {
        "license_plate": ["Vehicle with this license plate already exists."]
    }
}
```

---

### Get Vehicle Details
Retrieves details of a specific vehicle owned by the authenticated user.

**Endpoint:** `GET /vehicles/{id}/`  
**Authentication:** Required

#### Response (200 OK)
```json
{
    "id": 1,
    "make": "Toyota",
    "model": "Camry",
    "year": 2022,
    "license_plate": "ABC-123",
    "color": "Blue",
    "vehicle_type": "sedan",
    "owner": 1,
    "created_at": "2025-07-11T10:30:00Z",
    "updated_at": "2025-07-11T10:30:00Z"
}
```

#### Error Response (404 Not Found)
```json
{
    "detail": "Not found."
}
```

---

### Update Vehicle
Updates details of a specific vehicle owned by the authenticated user.

**Endpoint:** `PUT /vehicles/{id}/`  
**Authentication:** Required

#### Request Body
```json
{
    "make": "Toyota",
    "model": "Camry Hybrid",
    "year": 2022,
    "license_plate": "ABC-123",
    "color": "Silver",
    "vehicle_type": "sedan"
}
```

#### Response (200 OK)
```json
{
    "message": "Vehicle updated successfully",
    "vehicle": {
        "id": 1,
        "make": "Toyota",
        "model": "Camry Hybrid",
        "year": 2022,
        "license_plate": "ABC-123",
        "color": "Silver",
        "vehicle_type": "sedan",
        "owner": 1,
        "created_at": "2025-07-11T10:30:00Z",
        "updated_at": "2025-07-11T12:00:00Z"
    }
}
```

---

### Delete Vehicle
Deletes a specific vehicle owned by the authenticated user.

**Endpoint:** `DELETE /vehicles/{id}/`  
**Authentication:** Required

#### Response (200 OK)
```json
{
    "message": "Vehicle deleted successfully"
}
```

---

## Booking Management

### List User Bookings
Retrieves a list of bookings made by the authenticated user.

**Endpoint:** `GET /bookings/`  
**Authentication:** Required

#### Response (200 OK)
```json
{
    "bookings": [
        {
            "id": 1,
            "vehicle": {
                "id": 1,
                "make": "Toyota",
                "model": "Camry",
                "license_plate": "ABC-123"
            },
            "start_date": "2025-07-15T10:00:00Z",
            "end_date": "2025-07-18T10:00:00Z",
            "status": "confirmed",
            "total_cost": 150.00,
            "created_at": "2025-07-11T10:30:00Z"
        }
    ]
}
```

---

### Create Booking
Creates a new booking for the authenticated user.

**Endpoint:** `POST /bookings/`  
**Authentication:** Required

#### Request Body
```json
{
    "vehicle": 1,
    "start_date": "2025-07-20T09:00:00Z",
    "end_date": "2025-07-22T18:00:00Z",
    "notes": "Airport pickup required"
}
```

#### Response (201 Created)
```json
{
    "message": "Booking created successfully",
    "booking": {
        "id": 2,
        "vehicle": 1,
        "user": 1,
        "start_date": "2025-07-20T09:00:00Z",
        "end_date": "2025-07-22T18:00:00Z",
        "status": "pending",
        "total_cost": 120.00,
        "notes": "Airport pickup required",
        "created_at": "2025-07-11T13:00:00Z",
        "updated_at": "2025-07-11T13:00:00Z"
    }
}
```

#### Error Response (400 Bad Request)
```json
{
    "error": "Failed to create booking",
    "details": {
        "start_date": ["Start date cannot be in the past."],
        "vehicle": ["Vehicle is not available for the selected dates."]
    }
}
```

---

### Get Booking Details
Retrieves details of a specific booking owned by the authenticated user.

**Endpoint:** `GET /bookings/{id}/`  
**Authentication:** Required

#### Response (200 OK)
```json
{
    "id": 1,
    "vehicle": {
        "id": 1,
        "make": "Toyota",
        "model": "Camry",
        "license_plate": "ABC-123"
    },
    "user": 1,
    "start_date": "2025-07-15T10:00:00Z",
    "end_date": "2025-07-18T10:00:00Z",
    "status": "confirmed",
    "total_cost": 150.00,
    "notes": "Airport pickup required",
    "created_at": "2025-07-11T10:30:00Z",
    "updated_at": "2025-07-11T10:30:00Z"
}
```

---

### Update Booking
Updates details of a specific booking owned by the authenticated user.

**Endpoint:** `PUT /bookings/{id}/`  
**Authentication:** Required

#### Request Body
```json
{
    "start_date": "2025-07-15T08:00:00Z",
    "end_date": "2025-07-18T20:00:00Z",
    "notes": "Updated: Airport pickup and drop-off required"
}
```

#### Response (200 OK)
```json
{
    "message": "Booking updated successfully",
    "booking": {
        "id": 1,
        "vehicle": 1,
        "user": 1,
        "start_date": "2025-07-15T08:00:00Z",
        "end_date": "2025-07-18T20:00:00Z",
        "status": "confirmed",
        "total_cost": 160.00,
        "notes": "Updated: Airport pickup and drop-off required",
        "created_at": "2025-07-11T10:30:00Z",
        "updated_at": "2025-07-11T14:00:00Z"
    }
}
```

---

### Cancel Booking
Cancels a specific booking owned by the authenticated user.

**Endpoint:** `DELETE /bookings/{id}/`  
**Authentication:** Required

#### Response (200 OK)
```json
{
    "message": "Booking cancelled successfully"
}
```

---

## Dashboard

### Get User Statistics
Retrieves dashboard statistics for the authenticated user.

**Endpoint:** `GET /dashboard/stats/`  
**Authentication:** Required

#### Response (200 OK)
```json
{
    "stats": {
        "total_vehicles": 3,
        "total_bookings": 8,
        "active_bookings": 2,
        "pending_bookings": 1,
        "completed_bookings": 5,
        "total_spent": 450.00,
        "upcoming_bookings": [
            {
                "id": 3,
                "vehicle_name": "Toyota Camry",
                "start_date": "2025-07-20T09:00:00Z",
                "status": "confirmed"
            }
        ]
    }
}
```

---

## Data Models

### User
- `id`: Integer (Primary Key)
- `username`: String (Unique)
- `email`: String (Unique)
- `first_name`: String
- `last_name`: String
- `date_joined`: DateTime

### Vehicle
- `id`: Integer (Primary Key)
- `make`: String
- `model`: String
- `year`: Integer
- `license_plate`: String (Unique)
- `color`: String
- `vehicle_type`: String
- `owner`: Foreign Key (User)
- `created_at`: DateTime
- `updated_at`: DateTime

### Booking
- `id`: Integer (Primary Key)
- `vehicle`: Foreign Key (Vehicle)
- `user`: Foreign Key (User)
- `start_date`: DateTime
- `end_date`: DateTime
- `status`: String (pending, confirmed, completed, cancelled)
- `total_cost`: Decimal
- `notes`: Text
- `created_at`: DateTime
- `updated_at`: DateTime

---

## Status Codes

- `200 OK`: Successful GET, PUT requests
- `201 Created`: Successful POST requests
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required or invalid credentials
- `403 Forbidden`: Permission denied
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

---

## Error Handling

### Validation Errors
```json
{
    "error": "Validation failed",
    "details": {
        "field_name": ["Error message 1", "Error message 2"]
    }
}
```

### Authentication Errors
```json
{
    "detail": "Given token not valid for any token type",
    "code": "token_not_valid",
    "messages": [
        {
            "token_class": "AccessToken",
            "token_type": "access",
            "message": "Token is invalid or expired"
        }
    ]
}
```

---

## Rate Limiting
Currently no rate limiting is implemented. Consider implementing rate limiting for production use.

---

## Pagination
List endpoints use page number pagination with a default page size of 20 items.

**Pagination Response Format:**
```json
{
    "count": 100,
    "next": "http://127.0.0.1:8000/api/vehicles/?page=3",
    "previous": "http://127.0.0.1:8000/api/vehicles/?page=1",
    "results": [ ... ]
}
```

---

## Testing

### Using cURL
```bash
# Register
curl -X POST http://127.0.0.1:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@example.com","password":"pass123","password2":"pass123"}'

# Login
curl -X POST http://127.0.0.1:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"pass123"}'

# Create Vehicle (with token)
curl -X POST http://127.0.0.1:8000/api/vehicles/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"make":"Toyota","model":"Prius","year":2023,"license_plate":"TEST123","color":"White","vehicle_type":"hybrid"}'
```

### Using Python Requests
```python
import requests

# Base configuration
base_url = "http://127.0.0.1:8000/api"
headers = {"Content-Type": "application/json"}

# Register and get token
response = requests.post(f"{base_url}/register/", json={
    "username": "testuser",
    "email": "test@example.com", 
    "password": "testpass123",
    "password2": "testpass123"
})

token = response.json()["tokens"]["access"]
auth_headers = {**headers, "Authorization": f"Bearer {token}"}

# Create vehicle
vehicle_response = requests.post(f"{base_url}/vehicles/", 
    json={"make": "Toyota", "model": "Prius", "year": 2023, "license_plate": "TEST123"},
    headers=auth_headers
)
```

---

## Development Setup

1. **Install Dependencies:**
   ```bash
   pip install django djangorestframework djangorestframework-simplejwt
   ```

2. **Run Migrations:**
   ```bash
   python manage.py migrate
   ```

3. **Start Server:**
   ```bash
   python manage.py runserver
   ```

4. **Access Browsable API:**
   ```
   http://127.0.0.1:8000/api/
   ```

---

## Notes

- All timestamps are in UTC format
- JWT tokens expire after 1 hour (access) and 7 days (refresh)
- Vehicle ownership is automatically assigned to the authenticated user
- Bookings can only be made for vehicles owned by other users (booking system logic)
- Soft deletion may be implemented for vehicles and bookings

---

## About 1Now

1Now is a software company that provides digital solutions to the car rental businesses by providing them customized websites that are tailored according to their brand identity

It provides the following services:

- Real-time fleet tracking
- Automated bookings & payments  
- Expense tracking + profit insights
- Stripe & Square integration
- Analytics to grow your business

---

## Backend Integration with LahoreCarRental.com

This backend can be integrated with the frontend in the following ways:

- By enabling COARS and allowing the APIs to be consumed by all platforms
- Hosting the backend on a server so that the request can be made on the backend from anywhere in the world
- We can use Nginx and gunicorn to deploy our DRF backend on a Linux machine so that those APIs can be easily used in production

---

*Last updated: July 11, 2025*
