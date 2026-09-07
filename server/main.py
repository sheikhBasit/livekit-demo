import os
import uuid
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from livekit import api

load_dotenv()

LIVEKIT_URL = os.environ.get("LIVEKIT_URL", "")
LIVEKIT_API_KEY = os.environ.get("LIVEKIT_API_KEY", "")
LIVEKIT_API_SECRET = os.environ.get("LIVEKIT_API_SECRET", "")
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/livecall")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

from auth import router as auth_router, get_current_user
app.include_router(auth_router)

def get_db():
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    try:
        yield conn
    finally:
        conn.close()

class JoinRequest(BaseModel):
    user_id: str
    role: str

@app.post("/api/rooms/{class_id}/join")
def join_room(class_id: str, current_user: dict = Depends(get_current_user), db = Depends(get_db)):
    role = current_user['role']
    user_id = str(current_user['id'])

    if role not in ['teacher', 'student']:
        raise HTTPException(400, "Role must be teacher or student")
        
    cursor = db.cursor()
    # Ensure class exists (mocking it if it doesn't)
    cursor.execute("INSERT INTO classes (id, name) VALUES (%s, %s) ON CONFLICT DO NOTHING", (class_id, f"Class {class_id}"))
    
    
    # Look up or create room
    cursor.execute("SELECT * FROM rooms WHERE class_id = %s", (class_id,))
    room = cursor.fetchone()
    
    if not room:
        livekit_room_name = f"room_{class_id}"
        # We assume first person creating might be the teacher, or just assign null teacher for now
        cursor.execute(
            "INSERT INTO rooms (class_id, livekit_room_name) VALUES (%s, %s) RETURNING *",
            (class_id, livekit_room_name)
        )
        room = cursor.fetchone()
    
    livekit_room_name = room['livekit_room_name']
    
    if role == 'student':
        # Student waits
        cursor.execute(
            "INSERT INTO participants (user_id, role, status) VALUES (%s, %s, 'waiting') RETURNING id",
            (user_id, role)
        )
        participant_id = cursor.fetchone()['id']
        db.commit()
        return {"status": "waiting", "participant_id": participant_id}
        
    else:
        # Teacher joins immediately
        token = (
            api.AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET)
            .with_identity(user_id)
            .with_name(f"Teacher {user_id}")
            .with_grants(api.VideoGrants(
                room_join=True,
                room=livekit_room_name,
                room_admin=True,
                can_publish=True,
                can_subscribe=True,
                room_record=True
            ))
        )
        db.commit()
        return {"token": token.to_jwt(), "ws_url": LIVEKIT_URL, "status": "admitted"}

@app.get("/api/rooms/{class_id}/waiting")
def get_waiting_participants(class_id: str, current_user: dict = Depends(get_current_user), db = Depends(get_db)):
    cursor = db.cursor()
    # Join with room_sessions if we were using it, but for now we just filter by room
    cursor.execute("""
        SELECT p.id, p.user_id, p.role, p.status, u.name 
        FROM participants p 
        JOIN users u ON p.user_id = u.id 
        JOIN rooms r ON r.class_id = %s
        WHERE p.status = 'waiting'
    """, (class_id,))
    waiting = cursor.fetchall()
    return {"waiting": waiting}

@app.post("/api/rooms/{class_id}/admit/{participant_id}")
def admit_participant(class_id: str, participant_id: str, current_user: dict = Depends(get_current_user), db = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("UPDATE participants SET status = 'admitted' WHERE id = %s RETURNING *", (participant_id,))
    participant = cursor.fetchone()
    if not participant:
        raise HTTPException(404, "Participant not found")
        
    # Get room name
    cursor.execute("SELECT livekit_room_name FROM rooms WHERE class_id = %s", (class_id,))
    room = cursor.fetchone()
    if not room:
        raise HTTPException(404, "Room not found")
        
    db.commit()
    
    # Generate token for the admitted student
    token = (
        api.AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET)
        .with_identity(str(participant['user_id']))
        .with_name(f"Student {participant['user_id']}")
        .with_grants(api.VideoGrants(
            room_join=True,
            room=room['livekit_room_name'],
            room_admin=False,
            can_publish=True,
            can_publish_data=False,
            can_subscribe=True
        ))
    )
    
    return {"status": "admitted", "token": token.to_jwt()}

@app.get("/api/rooms/status/{participant_id}")
def check_participant_status(participant_id: str, room_id: str, current_user: dict = Depends(get_current_user), db = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT status, user_id FROM participants WHERE id = %s", (participant_id,))
    p = cursor.fetchone()
    if not p:
        raise HTTPException(404, "Participant not found")
        
    if p['status'] == 'admitted':
        cursor.execute("SELECT livekit_room_name FROM rooms WHERE class_id = %s", (room_id,))
        room = cursor.fetchone()
        
        token = (
            api.AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET)
            .with_identity(str(p['user_id']))
            .with_name(f"Student {p['user_id']}")
            .with_grants(api.VideoGrants(
                room_join=True,
                room=room['livekit_room_name'],
                room_admin=False,
                can_publish=True,
                can_publish_data=False,
                can_subscribe=True
            ))
        )
        return {"status": "admitted", "token": token.to_jwt(), "ws_url": LIVEKIT_URL}
        
    return {"status": p['status']}

from recording import start_recording_sync, stop_recording_sync
from fastapi import Request

@app.post("/api/rooms/{class_id}/start-session")
def start_session(class_id: str, current_user: dict = Depends(get_current_user), db = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT id, livekit_room_name FROM rooms WHERE class_id = %s", (class_id,))
    room = cursor.fetchone()
    if not room:
        raise HTTPException(404, "Room not found")
        
    egress_id = start_recording_sync(room['livekit_room_name'])
    
    cursor.execute(
        "INSERT INTO room_sessions (room_id, egress_id) VALUES (%s, %s) RETURNING *",
        (room['id'], egress_id)
    )
    session = cursor.fetchone()
    db.commit()
    return {"status": "started", "session_id": session['id']}

@app.post("/api/rooms/{class_id}/end-session")
def end_session(class_id: str, current_user: dict = Depends(get_current_user), db = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT id, livekit_room_name FROM rooms WHERE class_id = %s", (class_id,))
    room = cursor.fetchone()
    if not room:
        raise HTTPException(404, "Room not found")
        
    cursor.execute("SELECT id, egress_id FROM room_sessions WHERE room_id = %s AND ended_at IS NULL ORDER BY started_at DESC LIMIT 1", (room['id'],))
    session = cursor.fetchone()
    if not session:
        raise HTTPException(404, "Active session not found")
        
    if session['egress_id']:
        stop_recording_sync(session['egress_id'])
        
    cursor.execute("UPDATE room_sessions SET ended_at = NOW() WHERE id = %s", (session['id'],))
    db.commit()
    return {"status": "ended"}

@app.get("/api/admin/active-sessions")
def get_active_sessions(current_user: dict = Depends(get_current_user), db = Depends(get_db)):
    if current_user['role'] != 'admin':
        raise HTTPException(403, "Admin only")
    cursor = db.cursor()
    cursor.execute("""
        SELECT rs.id, r.livekit_room_name, rs.started_at, u.name as teacher_name
        FROM room_sessions rs
        JOIN rooms r ON rs.room_id = r.id
        JOIN users u ON r.teacher_id = u.id
        WHERE rs.ended_at IS NULL
    """)
    sessions = cursor.fetchall()
    return {"sessions": sessions}

@app.get("/api/admin/recordings")
def get_recordings(current_user: dict = Depends(get_current_user), db = Depends(get_db)):
    if current_user['role'] != 'admin':
        raise HTTPException(403, "Admin only")
    cursor = db.cursor()
    cursor.execute("""
        SELECT rec.id, rec.r2_key, rec.duration_seconds, rec.file_size_bytes, rec.created_at, u.name as teacher_name
        FROM recordings rec
        JOIN room_sessions rs ON rec.session_id = rs.id
        JOIN rooms r ON rs.room_id = r.id
        JOIN users u ON r.teacher_id = u.id
        ORDER BY rec.created_at DESC
    """)
    recordings = cursor.fetchall()
    return {"recordings": recordings}

@app.get("/api/admin/users")
def get_all_users(current_user: dict = Depends(get_current_user), db = Depends(get_db)):
    if current_user['role'] != 'admin':
        raise HTTPException(403, "Admin only")
    cursor = db.cursor()
    cursor.execute("SELECT id, name, email, role FROM users ORDER BY role, name")
    users = cursor.fetchall()
    return {"users": users}

@app.get("/api/teacher/history")
def get_teacher_history(current_user: dict = Depends(get_current_user), db = Depends(get_db)):
    if current_user['role'] != 'teacher':
        raise HTTPException(403, "Teacher only")
    cursor = db.cursor()
    cursor.execute("""
        SELECT rec.id, rec.duration_seconds, rec.ai_grade, rec.ai_feedback, rec.created_at
        FROM recordings rec
        JOIN room_sessions rs ON rec.session_id = rs.id
        JOIN rooms r ON rs.room_id = r.id
        WHERE r.teacher_id = %s
        ORDER BY rec.created_at DESC
    """, (current_user['sub'],))
    history = cursor.fetchall()
    return {"history": history}

from auth import get_password_hash

class AdminUserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: str

@app.post("/api/admin/users")
def create_user(user: AdminUserCreate, current_user: dict = Depends(get_current_user), db = Depends(get_db)):
    if current_user['role'] != 'admin':
        raise HTTPException(403, "Admin only")
    if user.role not in ['teacher', 'student', 'admin']:
        raise HTTPException(400, "Invalid role")
        
    cursor = db.cursor()
    cursor.execute("SELECT id FROM users WHERE email = %s", (user.email,))
    if cursor.fetchone():
        raise HTTPException(400, "Email already registered")
        
    hashed_password = get_password_hash(user.password)
    cursor.execute(
        "INSERT INTO users (name, email, password_hash, role) VALUES (%s, %s, %s, %s) RETURNING id, name, email, role",
        (user.name, user.email, hashed_password, user.role)
    )
    new_user = cursor.fetchone()
    db.commit()
    return {"user": new_user}

import os
import json
import random
import time
from fastapi import BackgroundTasks
from groq import Groq

# Initialize Groq Client
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

def run_ai_analysis(recording_id: str):
    if not groq_client:
        print("Groq API Key not found. Skipping real AI analysis.")
        return
        
    print(f"Starting Groq AI Analysis for recording {recording_id}...")
    
    # In a real app, you would download the video, extract audio, and transcribe it here.
    # We will use a realistic mock transcript for the evaluation prompt.
    mock_transcript = """
    Teacher: Welcome everyone to Biology 101. Today we are discussing cellular respiration. 
    Can anyone tell me the main organelle involved in this process?
    Student: Is it the mitochondria?
    Teacher: Excellent job! Yes, the mitochondria is the powerhouse of the cell. 
    Now, let's look at the three main stages: glycolysis, the Krebs cycle, and electron transport.
    """
    
    prompt = f"""
    You are an expert educational evaluator. Review the following class transcript and provide a grade (A, B, C, D, or F) and a brief, constructive feedback summary for the teacher.
    
    Transcript:
    {mock_transcript}
    
    Respond STRICTLY in JSON format with exactly two keys: "grade" (string) and "feedback" (string).
    """

    try:
        completion = groq_client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            response_format={"type": "json_object"}
        )
        
        response_json = json.loads(completion.choices[0].message.content)
        grade = response_json.get("grade", "Pending")
        feedback = response_json.get("feedback", "No feedback provided.")
        
        # Update db using a new connection since this runs in background
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE recordings SET ai_grade = %s, ai_feedback = %s WHERE id = %s",
            (grade, feedback, recording_id)
        )
        conn.commit()
        conn.close()
        print(f"✅ Groq AI Analysis completed for recording {recording_id}: Grade {grade}")
    except Exception as e:
        print(f"❌ Failed to run Groq analysis: {e}")

@app.post("/api/admin/analyze/{recording_id}")
def manual_analyze(recording_id: str, background_tasks: BackgroundTasks, current_user: dict = Depends(get_current_user), db = Depends(get_db)):
    if current_user['role'] != 'admin':
        raise HTTPException(403, "Admin only")
    background_tasks.add_task(run_ai_analysis, recording_id)
    return {"status": "Analysis queued", "recording_id": recording_id}

@app.post("/api/livekit/webhook")
async def receive_webhook(request: Request, background_tasks: BackgroundTasks, db = Depends(get_db)):
    body = await request.body()
    # In production, verify the webhook signature using LIVEKIT_API_SECRET
    import json
    try:
        event = json.loads(body)
    except:
        return {"status": "ignored"}
        
    if event.get("event") == "egress_ended":
        egress_info = event.get("egressInfo", {})
        egress_id = egress_info.get("egressId")
        
        # Get room_session based on egress_id
        cursor = db.cursor()
        cursor.execute("SELECT id FROM room_sessions WHERE egress_id = %s ORDER BY started_at DESC LIMIT 1", (egress_id,))
        session = cursor.fetchone()
        
        if session:
            # Assuming output is S3/R2, get the filepath from results
            results = egress_info.get("fileResults", [])
            key = results[0].get("filename", "unknown.mp4") if results else "unknown.mp4"
            duration = egress_info.get("duration", 0) // 1000000000 # ns to seconds
            size = results[0].get("size", 0) if results else 0
            
            cursor.execute(
                "INSERT INTO recordings (session_id, r2_key, duration_seconds, file_size_bytes) VALUES (%s, %s, %s, %s) RETURNING id",
                (session['id'], key, duration, size)
            )
            recording = cursor.fetchone()
            db.commit()
            print(f"Saved recording {recording['id']} for session {session['id']}")
            
            # Trigger AI pipeline automatically!
            background_tasks.add_task(run_ai_analysis, recording['id'])
            
    return {"status": "received"}
