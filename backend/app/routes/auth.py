from datetime import UTC, datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session  
from app.db.database import get_db
from app.models.user import User
from app.schemas.auth import UserCreate, UserLogin, ForgotPasswordRequest, ResetPasswordRequest
from app.schemas.profile import UserProfileResponse, UserProfileUpdate
from app.utils.response import success_response
from app.utils.logger import log_api_activity
from app.core.security import(
    get_current_user,
    hash_password, 
    verify_password, 
    create_access_token,
)  
import secrets

router = APIRouter(prefix="/auth", tags=["Auth"])

# User Register
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    new_user = User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password),
        status = "active"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return success_response(
        message = "User registered successfully!"
    )

# User Login
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        user.password,
        existing_user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
    
    if existing_user.status != "active":

        raise HTTPException(

        status_code=403,

        detail=f"Account is {existing_user.status}"

    )

    access_token = create_access_token(
        data={
            "id": existing_user.id,
            "username": existing_user.username,
            "email": existing_user.email,
            "role": existing_user.role,
            }
    )

    log_api_activity(

        db=db,

        user_id = existing_user.id,

        username= existing_user.username,

        endpoint="/auth/login",

        method="GET",

        status="SUCCESS"
    )

    return success_response(
    message="User Login successful!",
    data = {
        "username": existing_user.username,
        "access_token": access_token,
        "token_type": "bearer",
        "role": existing_user.role
    }
    )

# Foreget password
@router.post("/forgot-password")
def forgot_password(
    request: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(User.email == request.email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    token = secrets.token_urlsafe(32)

    user.reset_token = token
    user.reset_token_expiry = datetime.utcnow() + timedelta(minutes=15)

    db.commit()

    return success_response(
        message = "Password reset token generated!",
        data = {
            "reset_token": token
        }
    )

@router.post("/reset-password")
def reset_password(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.reset_token == request.token
    ).first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid token")

    if (not user.reset_token_expiry or datetime.utcnow() > user.reset_token_expiry):
        
        raise HTTPException(status_code=400,detail="Token expired")

    user.password = hash_password(request.new_password)

    user.reset_token = None
    user.reset_token_expiry = None

    db.commit()

    return success_response(
        message = "Password reset successful!"
    )

@router.get(
    "/profile",
    response_model=UserProfileResponse
)
def get_profile(

    current_user: User =
    Depends(get_current_user)

):
    return current_user

@router.put(
    "/profile",
    response_model=UserProfileResponse
)
def update_profile(

    payload: UserProfileUpdate,

    db: Session = Depends(get_db),

    current_user: User =
    Depends(get_current_user)

):
    current_user.username = payload.username
    current_user.email = payload.email

    
    db.commit()
    db.refresh(current_user)

    return current_user