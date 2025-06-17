from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from backend.core.sql import get_user_by_username, verify_user_password, SessionLocal
from backend.core.auth import create_access_token, get_current_user
from backend.core.rate_limit import limiter



router = APIRouter()


# --- MODELS ---
class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

# --- ENDPOINTS ---
@router.post("/login", response_model=TokenResponse)
@limiter.limit("10/minute")
def login(data: LoginRequest):
    db = SessionLocal()
    user = get_user_by_username(db, data.username)
    if not user or not verify_user_password(db, data.username, data.password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    token = create_access_token({"sub": data.username})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me")
@limiter.limit("10/minute")
def me(username: str = Depends(get_current_user)):
    db = SessionLocal()
    user = get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "username": user.username,
        "is_admin": user.is_admin,
        "prompt_limit": user.prompt_limit,
        "prompt_count": user.prompt_count,
    }

