import requests

BASE_URL = "http://localhost:8001/api/auth/signup"

users = [
    {"name": "Admin User", "email": "admin@academy.com", "password": "password", "role": "admin"},
    {"name": "Teacher One", "email": "teacher1@academy.com", "password": "password", "role": "teacher"},
    {"name": "Student One", "email": "student1@academy.com", "password": "password", "role": "student"},
]

for user in users:
    res = requests.post(BASE_URL, json=user)
    print(f"{user['email']}: {res.status_code} {res.text}")
