"""
Authentication router
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from typing import Dict, Any
from app.security import create_access_token, get_current_user, hash_password, verify_password
from app.database import get_supabase
from datetime import timedelta

router = APIRouter()

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: Dict[str, Any]

@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    """User login"""
    try:
        supabase = get_supabase()
        
        # Authenticate with Supabase
        auth_response = supabase.auth.sign_in_with_password({
            "email": request.email,
            "password": request.password
        })
        
        if auth_response.user:
            # Create our own JWT token
            token_data = {
                "sub": auth_response.user.id,
                "email": auth_response.user.email,
                "role": "user"
            }
            access_token = create_access_token(token_data)
            
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "user": {
                    "id": auth_response.user.id,
                    "email": auth_response.user.email,
                    "full_name": auth_response.user.user_metadata.get("full_name", "")
                }
            }
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")
            
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.post("/signup", response_model=TokenResponse)
async def signup(request: SignupRequest):
    """User signup"""
    try:
        supabase = get_supabase()
        
        # Create user in Supabase
        auth_response = supabase.auth.sign_up({
            "email": request.email,
            "password": request.password,
            "options": {
                "data": {
                    "full_name": request.full_name
                }
            }
        })
        
        if auth_response.user:
            # Create JWT token
            token_data = {
                "sub": auth_response.user.id,
                "email": auth_response.user.email,
                "role": "user"
            }
            access_token = create_access_token(token_data)
            
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "user": {
                    "id": auth_response.user.id,
                    "email": auth_response.user.email,
                    "full_name": request.full_name
                }
            }
        else:
            raise HTTPException(status_code=400, detail="Signup failed")
            
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/me")
async def get_current_user_info(current_user: Dict = Depends(get_current_user)):
    """Get current user info"""
    return {
        "user": current_user
    }

@router.post("/logout")
async def logout():
    """Logout (client should remove token)"""
    return {"message": "Logged out successfully"}
