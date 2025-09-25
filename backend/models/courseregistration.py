from pydantic import BaseModel
from typing import Optional
from datetime import date

class CourseRegistrationBase(BaseModel):
    CandidateID: int
    CohortID: int
    RegistrationDate: date
    PaymentStatus: Optional[str] = "Pending"     # Pending, Paid, Failed
    Status: Optional[str] = "Registered"         # Registered, InProgress, Completed, Withdrawn
    Result: Optional[str] = None
    CompletionDate: Optional[date] = None

class CourseRegistrationCreate(CourseRegistrationBase):
    pass

class CourseRegistration(CourseRegistrationBase):
    RegistrationID: int

    class Config:
        orm_mode = True
