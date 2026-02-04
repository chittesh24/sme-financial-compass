"""
Authentication router
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from typing import Dict, Any
from app.security import create_access_token, get_current_user
from app.database import get_supabase

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

        auth_response = supabase.auth.sign_in_with_password({
            "email": request.email,
            "password": request.password,
        })

        if not auth_response.user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        token_data = {
            "sub": auth_response.user.id,
            "email": auth_response.user.email,
            "role": "user",
        }

        access_token = create_access_token(token_data)

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": auth_response.user.id,
                "email": auth_response.user.email,
                "full_name": auth_response.user.user_metadata.get("full_name", ""),
            },
        }

    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.post("/signup", response_model=TokenResponse)
async def signup(request: SignupRequest):
    """User signup"""
    try:
        supabase = get_supabase()

        auth_response = supabase.auth.sign_up({
            "email": request.email,
            "password": request.password,
            "options": {
                "data": {
                    "full_name": request.full_name
                }
            },
        })

        if not auth_response.user:
            raise HTTPException(status_code=400, detail="Signup failed")

        token_data = {
            "sub": auth_response.user.id,
            "email": auth_response.user.email,
            "role": "user",
        }

        access_token = create_access_token(token_data)

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": auth_response.user.id,
                "email": auth_response.user.email,
                "full_name": request.full_name,
                "email_confirmed": auth_response.user.email_confirmed_at is not None,
            },
        }

    except Exception as e:
        error_message = str(e).lower()

        if "already registered" in error_message:
            raise HTTPException(
                status_code=400,
                detail="Email already registered. Please sign in.",
            )
        elif "weak password" in error_message:
            raise HTTPException(
                status_code=400,
                detail="Password too weak. Use at least 6 characters.",
            )

        raise HTTPException(status_code=400, detail=str(e))


@router.get("/me")
async def get_current_user_info(current_user: Dict = Depends(get_current_user)):
    return {"user": current_user}


@router.post("/logout")
async def logout(current_user: Dict = Depends(get_current_user)):
    """Logout endpoint"""
    return {
        "message": "Logged out successfully",
        "user_id": current_user.get("user_id"),
    }
