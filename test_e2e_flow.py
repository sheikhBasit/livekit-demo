import requests
import time

import uuid

BASE_URL = "http://localhost:8001/api"
CLASS_ID = str(uuid.uuid4())

def run_test():
    print("Starting E2E API Flow Test...")

    # 1. Login Teacher
    print("\n1. Logging in Teacher...")
    res = requests.post(f"{BASE_URL}/auth/login", json={"email": "teacher1@academy.com", "password": "password"})
    assert res.status_code == 200, f"Teacher login failed: {res.text}"
    teacher_token = res.json()["access_token"]
    teacher_headers = {"Authorization": f"Bearer {teacher_token}"}
    print("Teacher login successful.")

    # 2. Login Student
    print("\n2. Logging in Student...")
    res = requests.post(f"{BASE_URL}/auth/login", json={"email": "student1@academy.com", "password": "password"})
    assert res.status_code == 200, "Student login failed"
    student_token = res.json()["access_token"]
    student_headers = {"Authorization": f"Bearer {student_token}"}
    print("Student login successful.")

    # 3. Student Joins Class (enters waiting room)
    print("\n3. Student joining class...")
    res = requests.post(f"{BASE_URL}/rooms/{CLASS_ID}/join", headers=student_headers, json={})
    assert res.status_code == 200, f"Student join failed: {res.text}"
    join_data = res.json()
    assert join_data["status"] == "waiting", "Student should be in waiting status"
    participant_id = join_data["participant_id"]
    print(f"Student joined and is waiting. Participant ID: {participant_id}")

    # 4. Teacher Joins Class
    print("\n4. Teacher joining class...")
    res = requests.post(f"{BASE_URL}/rooms/{CLASS_ID}/join", headers=teacher_headers, json={})
    assert res.status_code == 200, "Teacher join failed"
    assert res.json()["status"] == "admitted", "Teacher should be admitted immediately"
    print("Teacher joined successfully.")

    # 5. Teacher checks waiting room
    print("\n5. Teacher checking waiting room...")
    res = requests.get(f"{BASE_URL}/rooms/{CLASS_ID}/waiting", headers=teacher_headers)
    assert res.status_code == 200, "Failed to get waiting list"
    waiting = res.json().get("waiting", [])
    assert len(waiting) > 0, "Waiting list should not be empty"
    assert waiting[0]["id"] == participant_id, "Student not found in waiting list"
    print("Student found in waiting room.")

    # 6. Teacher admits student
    print("\n6. Teacher admitting student...")
    res = requests.post(f"{BASE_URL}/rooms/{CLASS_ID}/admit/{participant_id}", headers=teacher_headers)
    assert res.status_code == 200, "Failed to admit student"
    print("Student admitted.")

    # 7. Student checks status
    print("\n7. Student checking admission status...")
    res = requests.get(f"{BASE_URL}/rooms/status/{participant_id}?room_id={CLASS_ID}", headers=student_headers)
    assert res.status_code == 200, "Failed to check status"
    status_data = res.json()
    assert status_data["status"] == "admitted", "Student should be admitted now"
    assert "token" in status_data, "LiveKit token should be provided"
    print("Student received LiveKit token.")

    # 8. Teacher starts session (Recording triggers)
    print("\n8. Teacher starting session (triggering egress)...")
    res = requests.post(f"{BASE_URL}/rooms/{CLASS_ID}/start-session", headers=teacher_headers)
    assert res.status_code == 200, "Failed to start session"
    print("Session started.")

    # 9. Teacher ends session
    print("\n9. Teacher ending session (stopping egress)...")
    res = requests.post(f"{BASE_URL}/rooms/{CLASS_ID}/end-session", headers=teacher_headers)
    assert res.status_code == 200, "Failed to end session"
    print("Session ended.")

    print("\n10. Faking webhook for AI analysis...")
    # Fetch session ID for webhook mock
    session_id = res.json().get("session_id")
    # For testing, we can hit the manual analyze endpoint instead of digging out egress_id
    # We need an admin token for that
    print("Logging in Admin...")
    admin_res = requests.post(f"{BASE_URL}/auth/login", json={"email": "admin@academy.com", "password": "password"})
    admin_token = admin_res.json()["access_token"]
    
    # We will trigger webhook directly simulating livekit
    webhook_payload = {
        "event": "egress_ended",
        "egressInfo": {
            "egressId": "mock-egress", # In actual test we might not have it unless we query db
            "duration": 3600000000000,
            "fileResults": [{"filename": "e2e_test.mp4", "size": 1024}]
        }
    }
    
    # Wait! The easiest way is just to manually create a mock egress_id in our start-session
    # Since start_session doesn't return egress_id, let's just query the db via a small hack or 
    # instead we can just hit the /admin/recordings endpoint after mocking it.
    
    # Let's simplify and just rely on the test_api_comprehensive script I made earlier,
    # or I can just use Python's psycopg2 directly in this script to fetch it!
    import psycopg2
    from psycopg2.extras import RealDictCursor
    conn = psycopg2.connect("postgresql://postgres:postgres@localhost:5445/livecall", cursor_factory=RealDictCursor)
    cur = conn.cursor()
    cur.execute("SELECT id, egress_id FROM room_sessions ORDER BY started_at DESC LIMIT 1")
    last_session = cur.fetchone()
    webhook_payload["egressInfo"]["egressId"] = last_session["egress_id"]
    
    print("Sending webhook payload:", webhook_payload)
    res = requests.post(f"{BASE_URL}/livekit/webhook", json=webhook_payload)
    assert res.status_code == 200, f"Webhook failed: {res.text}"
    
    print("Waiting for background AI task...")
    
    recording = None
    for _ in range(10):
        time.sleep(1)
        cur.execute("SELECT * FROM recordings WHERE session_id = %s", (last_session["id"],))
        recording = cur.fetchone()
        if recording and recording["ai_grade"] is not None:
            break
            
    assert recording is not None, "Recording was not inserted"
    assert recording["ai_grade"] is not None, "AI Grade was not assigned"
    print(f"Verified AI Output! Grade: {recording['ai_grade']}, Feedback: {recording['ai_feedback']}")

    print("\n✅ E2E API Flow Test Completed Successfully!")

if __name__ == "__main__":
    run_test()
