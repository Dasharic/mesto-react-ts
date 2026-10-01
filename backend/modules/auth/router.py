from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database import get_db
from typing import Optional

router = APIRouter(prefix="/api/auth", tags=["auth"])

class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str

class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    avatar: Optional[str] = None

@router.post("/login")
def login(data: LoginRequest):
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE email=? AND password=?", (data.email, data.password)).fetchone()
    if user:
        return {
            "token": f"token_{user['email']}",
            "role": user["role"],
            "profile": {"name": user["profile_name"], "email": user["email"], "avatar": user["profile_avatar"]}
        }
    raise HTTPException(status_code=400, detail="Неверный email или пароль")

@router.post("/register")
def register(data: RegisterRequest):
    conn = get_db()
    existing = conn.execute("SELECT email FROM users WHERE email=?", (data.email,)).fetchone()
    if existing:
        raise HTTPException(status_code=400, detail="Пользователь с таким email уже существует")
    
    conn.execute("INSERT INTO users (email, password, role, profile_name, profile_avatar) VALUES (?, ?, ?, ?, ?)",
                 (data.email, data.password, "user", data.name, ""))
    conn.commit()
    
    return {
        "token": f"token_{data.email}",
        "role": "user",
        "profile": {"name": data.name, "email": data.email, "avatar": ""}
    }

@router.get("/me")
def get_me(token: str):
    email = token.replace("token_", "")
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
    if user:
        return {"role": user["role"], "profile": {"name": user["profile_name"], "email": user["email"], "avatar": user["profile_avatar"]}}
    raise HTTPException(status_code=401, detail="Неверный токен")

@router.patch("/me")
def update_profile(token: str, data: ProfileUpdate):
    email = token.replace("token_", "")
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
    if not user:
        raise HTTPException(status_code=401, detail="Неверный токен")
        
    name = data.name if data.name is not None else user["profile_name"]
    avatar = data.avatar if data.avatar is not None else user["profile_avatar"]
    
    conn.execute("UPDATE users SET profile_name=?, profile_avatar=? WHERE email=?", (name, avatar, email))
    conn.commit()
    return {"status": "ok"}
