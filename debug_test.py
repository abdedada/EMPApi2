import requests
import json

BASE_URL = "http://localhost:8000"

print("Testing /auth/register...")
response = requests.post(
    f"{BASE_URL}/auth/register",
    json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "TestPass123"
    }
)

print(f"Status Code: {response.status_code}")
print(f"Headers: {dict(response.headers)}")
print(f"Response Text: {response.text}")

try:
    print(f"JSON: {response.json()}")
except:
    print("Could not parse JSON")

