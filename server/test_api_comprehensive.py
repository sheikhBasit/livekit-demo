import pytest
from fastapi.testclient import TestClient
from main import app, get_db
import uuid

client = TestClient(app)
CLASS_ID = str(uuid.uuid4())
TEACHER_EMAIL = "teacher1@academy.com"
STUDENT_EMAIL = "student1@academy.com"
ADMIN_EMAIL = "admin@academy.com"
PASSWORD = "password"

def test_login_success():
    response = client.post("/api/auth/login", json={"email": TEACHER_EMAIL, "password": PASSWORD})
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["user"]["role"] == "teacher"

def test_login_fail_wrong_password():
    response = client.post("/api/auth/login", json={"email": TEACHER_EMAIL, "password": "wrong"})
    assert response.status_code == 401

def test_login_fail_nonexistent_user():
    response = client.post("/api/auth/login", json={"email": "nobody@academy.com", "password": PASSWORD})
    assert response.status_code == 401

def test_unauthorized_access():
    response = client.post(f"/api/rooms/{CLASS_ID}/join", json={})
    assert response.status_code == 401

def test_teacher_join_room():
    # Login
    res = client.post("/api/auth/login", json={"email": TEACHER_EMAIL, "password": PASSWORD})
    token = res.json()["access_token"]
    
    # Join
    join_res = client.post(f"/api/rooms/{CLASS_ID}/join", headers={"Authorization": f"Bearer {token}"})
    assert join_res.status_code == 200
    assert join_res.json()["status"] == "admitted"
    assert "token" in join_res.json()

def test_student_join_room_waiting():
    # Login
    res = client.post("/api/auth/login", json={"email": STUDENT_EMAIL, "password": PASSWORD})
    token = res.json()["access_token"]
    
    # Join
    join_res = client.post(f"/api/rooms/{CLASS_ID}/join", headers={"Authorization": f"Bearer {token}"})
    assert join_res.status_code == 200
    assert join_res.json()["status"] == "waiting"
    assert "participant_id" in join_res.json()
    
    return join_res.json()["participant_id"]

def test_teacher_check_waiting_and_admit():
    # First student joins
    participant_id = test_student_join_room_waiting()
    
    # Teacher logs in
    res = client.post("/api/auth/login", json={"email": TEACHER_EMAIL, "password": PASSWORD})
    token = res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Check waiting
    wait_res = client.get(f"/api/rooms/{CLASS_ID}/waiting", headers=headers)
    assert wait_res.status_code == 200
    waiting = wait_res.json().get("waiting", [])
    assert any(p["id"] == participant_id for p in waiting)
    
    # Admit
    admit_res = client.post(f"/api/rooms/{CLASS_ID}/admit/{participant_id}", headers=headers)
    assert admit_res.status_code == 200
    assert admit_res.json()["status"] == "admitted"
    assert "token" in admit_res.json()

def test_student_check_status_after_admit():
    # First student joins
    participant_id = test_student_join_room_waiting()
    
    # Student token
    res = client.post("/api/auth/login", json={"email": STUDENT_EMAIL, "password": PASSWORD})
    student_headers = {"Authorization": f"Bearer {res.json()['access_token']}"}
    
    # Check status before admit
    status_res = client.get(f"/api/rooms/status/{participant_id}?room_id={CLASS_ID}", headers=student_headers)
    assert status_res.status_code == 200
    assert status_res.json()["status"] == "waiting"
    
    # Teacher admits
    res_t = client.post("/api/auth/login", json={"email": TEACHER_EMAIL, "password": PASSWORD})
    client.post(f"/api/rooms/{CLASS_ID}/admit/{participant_id}", headers={"Authorization": f"Bearer {res_t.json()['access_token']}"})
    
    # Check status after admit
    status_res = client.get(f"/api/rooms/status/{participant_id}?room_id={CLASS_ID}", headers=student_headers)
    assert status_res.status_code == 200
    assert status_res.json()["status"] == "admitted"
    assert "token" in status_res.json()

def test_session_lifecycle():
    # Login Teacher
    res = client.post("/api/auth/login", json={"email": TEACHER_EMAIL, "password": PASSWORD})
    token = res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Teacher joins to initialize room record
    client.post(f"/api/rooms/{CLASS_ID}/join", headers=headers)
    
    # Start session
    start_res = client.post(f"/api/rooms/{CLASS_ID}/start-session", headers=headers)
    assert start_res.status_code == 200
    assert start_res.json()["status"] == "started"
    
    # End session
    end_res = client.post(f"/api/rooms/{CLASS_ID}/end-session", headers=headers)
    assert end_res.status_code == 200
    assert end_res.json()["status"] == "ended"

