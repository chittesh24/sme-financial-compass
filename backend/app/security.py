"""
Security utilities: JWT, encryption, authentication
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from cryptography.fernet import Fernet
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import base64
import hashlib
from app.config import settings

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Security
security = HTTPBearer()

# Encryption for sensitive data (banking tokens, etc.)
def get_encryption_key() -> bytes:
    """Generate encryption key from settings"""
    if settings.ENCRYPTION_KEY:
        # Use provided key
        key = hashlib.sha256(settings.ENCRYPTION_KEY.encode()).digest()
        return base64.urlsafe_b64encode(key)
    else:
        # Generate from SECRET_KEY
        key = hashlib.sha256(settings.SECRET_KEY.encode()).digest()
        return base64.urlsafe_b64encode(key)

fernet = Fernet(get_encryption_key())

def hash_password(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash"""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Dict[str, Any]:
    """Decode and verify JWT token"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """Get current authenticated user from JWT token"""
    token = credentials.credentials
    payload = decode_access_token(token)
    
    user_id: str = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
    
    return {
        "user_id": user_id,
        "email": payload.get("email"),
        "role": payload.get("role", "user")
    }

def encrypt_sensitive_data(data: str) -> str:
    """Encrypt sensitive data (banking tokens, API keys, etc.)"""
    if not data:
        return ""
    encrypted = fernet.encrypt(data.encode())
    return encrypted.decode()

def decrypt_sensitive_data(encrypted_data: str) -> str:
    """Decrypt sensitive data"""
    if not encrypted_data:
        return ""
    decrypted = fernet.decrypt(encrypted_data.encode())
    return decrypted.decode()

def sanitize_input(text: str, max_length: int = 1000) -> str:
    """Sanitize user input to prevent injection attacks"""
    if not text:
        return ""
    
    # Remove potentially dangerous characters
    dangerous_chars = ['<', '>', '"', "'", '`', ';', '--', '/*', '*/']
    sanitized = text
    for char in dangerous_chars:
        sanitized = sanitized.replace(char, '')
    
    # Limit length
    return sanitized[:max_length].strip()

def validate_file_type(filename: str) -> bool:
    """Validate uploaded file type"""
    import os
    _, ext = os.path.splitext(filename.lower())
    return ext in settings.ALLOWED_EXTENSIONS

def validate_file_size(file_size: int) -> bool:
    """Validate uploaded file size"""
    return file_size <= settings.MAX_UPLOAD_SIZE
