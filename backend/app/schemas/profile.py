from pydantic import BaseModel, EmailStr


class UserProfileResponse(BaseModel):

    id: int
    username: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True


class UserProfileUpdate(BaseModel):

    username: str
    email: EmailStr
