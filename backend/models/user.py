from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    CentreID: Optional[int] = None
    FirstName: str
    LastName: str
    Email: str
    PasswordHash: str  # normally you'd hash this properly!
    Role: str  # must be one of: AccreditationStaff, CentreStaff, Instructor
    IsActive: Optional[bool] = True

class UserCreate(UserBase):
    pass

class User(UserBase):
    UserID: int

    class Config:
        orm_mode = True
