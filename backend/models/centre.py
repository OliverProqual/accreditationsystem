from pydantic import BaseModel
from typing import Optional

class CentreBase(BaseModel):
    CentreName: str
    Address: Optional[str] = None
    ContactEmail: Optional[str] = None
    ContactPhone: Optional[str] = None
    IsActive: Optional[bool] = True

class CentreCreate(CentreBase):
    pass

class Centre(CentreBase):
    CentreID: int

    class Config:
        orm_mode = True
