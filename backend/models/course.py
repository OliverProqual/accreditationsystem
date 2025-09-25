from pydantic import BaseModel
from typing import Optional

class CourseBase(BaseModel):
    CourseCode: str
    CourseName: str
    Description: Optional[str] = None
    DurationWeeks: Optional[int] = None
    CertificateID: int

class CourseCreate(CourseBase):
    pass

class Course(CourseBase):
    CourseID: int

    class Config:
        orm_mode = True
