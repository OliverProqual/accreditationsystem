from pydantic import BaseModel
from typing import Optional

class CertificateBase(BaseModel):
    CertificateName: str
    Level: Optional[str] = None
    Description: Optional[str] = None

class CertificateCreate(CertificateBase):
    pass

class Certificate(CertificateBase):
    CertificateID: int

    class Config:
        orm_mode = True
