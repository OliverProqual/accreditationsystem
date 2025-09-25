from fastapi import APIRouter
from models.certificate import CertificateCreate, Certificate
import crud.certificate as crud

router = APIRouter(prefix="/centres", tags=["centres"])

@router.post("/certificates", response_model=Certificate)
def create_certificate(cert: CertificateCreate):
    return crud.create_certificate(cert)


@router.get("/certificates/{certificate_id}", response_model=Certificate)
def get_certificate(certificate_id: int):
    return crud.get_certificate(certificate_id)


@router.get("/certificates", response_model=list[Certificate])
def list_certificates(limit: int = 10):
    return crud.list_certificates(limit)
    
@router.put("/certificates/{certificate_id}", response_model=Certificate)
def update_certificate(certificate_id: int, cert: CertificateCreate):
    return crud.update_certificate(certificate_id, cert)


@router.delete("/certificates/{certificate_id}")
def delete_certificate(certificate_id: int):
    return crud.delete_certificate(certificate_id)
