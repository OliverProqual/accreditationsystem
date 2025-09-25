from pydantic import BaseModel
from typing import Optional
from datetime import date

class IssuedCertificateBase(BaseModel):
    RegistrationID: int
    CertificateNumber: str
    IssueDate: date
    ExpiryDate: Optional[date] = None
    Status: Optional[str] = "Valid"   # Valid, Expired, Revoked

class IssuedCertificateCreate(IssuedCertificateBase):
    pass

class IssuedCertificate(IssuedCertificateBase):
    IssueID: int

    class Config:
        orm_mode = True
