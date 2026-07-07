from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException
from jose import jwt
from app.core.config import settings
 
router = APIRouter(prefix="/auth", tags=["auth"])
 
@router.post("/login")
def login(username: str, password: str):
    # v1: single operator account from env vars; full user table is a stretch item
    if username != settings.admin_user or password != settings.admin_password:
        raise HTTPException(401, "Invalid credentials")
    expire = datetime.utcnow() + timedelta(minutes=settings.jwt_expire_minutes)
    token = jwt.encode({"sub": username, "exp": expire}, settings.jwt_secret, algorithm="HS256")
    return {"access_token": token, "token_type": "bearer"}
