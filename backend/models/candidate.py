from pydantic import BaseModel
from typing import Optional
from datetime import date

class CandidateBase(BaseModel):
    PersonUID: str
    FirstName: str
    LastName: str
    NINumber: Optional[str] = None
    Gender: Optional[str] = None
    Ethnicity: Optional[str] = None
    DateOfBirth: Optional[date] = None
    CentreID: int

class CandidateCreate(CandidateBase):
    pass

class Candidate(CandidateBase):
    CandidateID: int

    class Config:
        orm_mode = True