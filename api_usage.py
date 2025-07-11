import requests
access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUyMjQ3NTA4LCJpYXQiOjE3NTIyNDM5MDgsImp0aSI6ImRmNzY3NWI1NGQxYzQwZTk5ZWY4NTVjYjUyMjcxOTIxIiwidXNlcl9pZCI6MX0.apV6_gT2ucselRT0mvgVeUvo09_3hvO5XovbCZxoq7o"
vehicle_url = "http://127.0.0.1:8000/api/vehicles/"
vehicle_data = {
    "make": "Toyota",
    "model": "Camry",
    "year": 2022,
    "plate": "ABC123", 
    "color": "Blue",
    "vehicle_type": "sedan"
}

booking_url = "http://127.0.0.1:8000/api/bookings/"
booking_data = {
    "vehicle": 1,
    "start_date": "2025-07-15T10:00:00Z",
    "end_date": "2025-07-18T10:00:00Z",
}

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

# response = requests.post(vehicle_url, json=vehicle_data, headers=headers)
# print(response.status_code)
# print(response.json())

response = requests.post(booking_url, json=booking_data, headers=headers)
print(response.status_code)
print(response.json())