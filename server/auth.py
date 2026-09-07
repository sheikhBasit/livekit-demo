import os
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import jwt
from psycopg2.extras import RealDictCursor
import psycopg2

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/livecall")
SECRET_KEY = os.environ.get("SECRET_KEY", "supersecretkey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 1 week

router = APIRouter(prefix="/api/auth")

def get_db():
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    try:
        yield conn
    finally:
        conn.close()

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: str

class UserLogin(BaseModel):
    email: str
    password: str

import bcrypt

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def get_password_hash(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/signup")
def signup(user: UserCreate, db = Depends(get_db)):
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
    
    token = create_access_token({"sub": str(new_user['id']), "role": new_user['role']})
    return {"access_token": token, "user": new_user}

@router.post("/login")
def login(user: UserLogin, db = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s", (user.email,))
    db_user = cursor.fetchone()
    
    if not db_user or not verify_password(user.password, db_user['password_hash']):
        raise HTTPException(401, "Invalid credentials")
        
    token = create_access_token({"sub": str(db_user['id']), "role": db_user['role']})
    return {
        "access_token": token, 
        "user": {
            "id": str(db_user['id']),
            "name": db_user['name'],
            "email": db_user['email'],
            "role": db_user['role']
        }
    }

from fastapi import Header
def get_current_user(authorization: str = Header(None), db = Depends(get_db)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401, "Invalid or missing token")
        
    token = authorization.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(401, "Invalid token")
    except jwt.PyJWTError:
        raise HTTPException(401, "Invalid token")
        
    cursor = db.cursor()
    cursor.execute("SELECT id, name, email, role FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    if not user:
        raise HTTPException(401, "User not found")
        
    return user
