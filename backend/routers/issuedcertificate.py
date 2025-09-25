from fastapi import APIRouter
from models.issuedcertificate import IssuedCertificateCreate, IssuedCertificate
import crud.issuedcertificate as crud

router = APIRouter(prefix="/centres", tags=["centres"])

@router.post("/issuedcertificates", response_model=IssuedCertificate)
def create_issued_certificate(cert: IssuedCertificateCreate):
    return crud.create_issued_certificate(cert)


@router.get("/issuedcertificates/{issue_id}", response_model=IssuedCertificate)
def get_issued_certificate(issue_id: int):
    return crud.get_issued_certificate(issue_id)


@router.get("/issuedcertificates", response_model=list[IssuedCertificate])
def list_issued_certificates(limit: int = 10):
    return crud.list_issued_certificates(limit)
    
@router.put("/issuedcertificates/{issue_id}", response_model=IssuedCertificate)
def update_issued_certificate(issue_id: int, cert: IssuedCertificateCreate):
    return crud.update_issued_certificate(issue_id, cert)


@router.delete("/issuedcertificates/{issue_id}")
def delete_issued_certificate(issue_id: int):
    return crud.delete_issued_certificate(issue_id)
