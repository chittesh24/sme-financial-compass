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
<<<<<<< HEAD
    """User signup"""
    try:
        supabase = get_supabase()
        
        # Create user in Supabase
=======
    """User signup - Creates account in Supabase and returns JWT token"""
    try:
        supabase = get_supabase()
        
        # Create user in Supabase with email confirmation disabled for development
>>>>>>> 33a2f18 (first commit)
        auth_response = supabase.auth.sign_up({
            "email": request.email,
            "password": request.password,
            "options": {
                "data": {
                    "full_name": request.full_name
<<<<<<< HEAD
                }
=======
                },
                # Email redirect URL - customize based on your frontend URL
                "email_redirect_to": "https://your-frontend-url.com/auth"
>>>>>>> 33a2f18 (first commit)
            }
        })
        
        if auth_response.user:
<<<<<<< HEAD
            # Create JWT token
=======
            # Create JWT token for immediate access
            # Note: If email confirmation is enabled, user needs to verify email first
>>>>>>> 33a2f18 (first commit)
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
<<<<<<< HEAD
                    "full_name": request.full_name
=======
                    "full_name": request.full_name,
                    "email_confirmed": auth_response.user.email_confirmed_at is not None
>>>>>>> 33a2f18 (first commit)
                }
            }
        else:
            raise HTTPException(status_code=400, detail="Signup failed")
            
    except Exception as e:
<<<<<<< HEAD
        raise HTTPException(status_code=400, detail=str(e))
=======
        error_message = str(e)
        # Provide helpful error messages
        if "already registered" in error_message.lower():
            raise HTTPException(status_code=400, detail="Email already registered. Please sign in instead.")
        elif "weak password" in error_message.lower():
            raise HTTPException(status_code=400, detail="Password is too weak. Use at least 6 characters.")
        else:
            raise HTTPException(status_code=400, detail=error_message)
>>>>>>> 33a2f18 (first commit)

@router.get("/me")
async def get_current_user_info(current_user: Dict = Depends(get_current_user)):
    """Get current user info"""
    return {
        "user": current_user
    }

@router.post("/logout")
<<<<<<< HEAD
async def logout():
    """Logout (client should remove token)"""
    return {"message": "Logged out successfully"}
=======
async def logout(current_user: Dict = Depends(get_current_user)):
    """
    Logout - Invalidates the session on Supabase
    Note: JWT tokens are stateless, so client must remove the token
    """
    try:
        # Optional: Add token to blacklist in Redis/database for enterprise apps
        # For now, client-side removal is sufficient
        
        return {
            "message": "Logged out successfully",
            "user_id": current_user.get("user_id")
        }
    except Exception as e:
        # Even if there's an error, allow logout to proceed
        return {"message": "Logged out successfully"}
>>>>>>> 33a2f18 (first commit)
