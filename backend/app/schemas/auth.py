from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str    

class ForgotPasswordRequest(BaseModel):
    email: str    

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str        

class UserStatusUpdate(BaseModel):
    status: str    

class UserRoleOrganizationUpdate(BaseModel):
    role: str
    organization_id: int | None = None
