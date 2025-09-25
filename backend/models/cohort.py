from pydantic import BaseModel
from typing import Optional
from datetime import date

class CohortBase(BaseModel):
    CentreID: int
    CourseID: int
    InstructorID: Optional[int] = None
    StartDate: date
    EndDate: Optional[date] = None

class CohortCreate(CohortBase):
    pass

class Cohort(CohortBase):
    CohortID: int

    class Config:
        orm_mode = True