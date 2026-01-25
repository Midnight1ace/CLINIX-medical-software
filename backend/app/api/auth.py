"""Authentication API Routes"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.services.auth_service import authenticate_user
from app.utils.validation import validate_email, validate_password

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str
    hospital_id: str

class TokenVerifyRequest(BaseModel):
    token: str

@router.post("/login")
async def login(request: LoginRequest):
    """Authenticate user and return token"""

    # Validate input
    if not validate_email(request.username):
        raise HTTPException(status_code=400, detail="Invalid email format")

    # Authenticate
    result = authenticate_user(request.username, request.password)
    if result['success']:
        return result
    else:
        raise HTTPException(status_code=401, detail=result.get('error', 'Authentication failed'))

@router.post("/verify-token")
async def verify_token(request: TokenVerifyRequest):
    """Verify JWT token validity"""
    from app.services.auth_service import validate_token

    result = validate_token(request.token)
    if result['valid']:
        return result
    else:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/logout")
async def logout():
    """Logout user (token invalidation on frontend)"""
    return {"message": "Logged out successfully"}
