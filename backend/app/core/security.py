from passlib.context import CryptContext
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
from jose import jwt, JWTError
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.models.user import User
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.session import SessionLocal

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(
        plain_password,
        hashed_password
    )

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt

security = HTTPBearer()

def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        email = payload.get("email")

        if email is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        return payload

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )
    
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("TOKEN PAYLOAD:", payload)   
        email = payload.get("email")

        if email is None:
            raise HTTPException(
            status_code=401,
            detail="Invalid token"
    )

        user = db.query(User).filter(User.email == email).first()

        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
        
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

def verify_role(role_type: str):

    allowed_roles = []

    match(role_type):

        case "admin":
            allowed_roles = ["super_admin"]

        case "admins":
            allowed_roles = ["super_admin", "organization_admin"]

        case "manager":
            allowed_roles = ["super_admin", "organization_admin", "manager"]

        case "analyst":
            allowed_roles = ["super_admin", "organization_admin", "analyst"]

        case "team":
            allowed_roles = ["super_admin", "organization_admin", "manager", "analyst"]

        case "all":
            allowed_roles = ["super_admin", "organization_admin", "manager", "analyst", "viewer"]

    def role_checker(user = Depends(verify_token)):
        
        if user.get("role") not in allowed_roles:

            raise HTTPException(
                status_code=403,
                detail="Access denied!"
            )

        return user
    return role_checker


                


