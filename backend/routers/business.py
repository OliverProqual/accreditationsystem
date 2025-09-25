# routers/business.py

from fastapi import APIRouter, Depends, HTTPException
from typing import List
from models.candidate import Candidate
from models.centre import Centre, CentreCreate
from models.course import Course, CourseCreate
from models.certificate import Certificate, CertificateCreate
from models.cohort import Cohort
from models.user import User
from models.courseregistration import CourseRegistrationCreate, CourseRegistration
from models.issuedcertificate import IssuedCertificateCreate, IssuedCertificate
import crud.business as crud
from routers.auth import get_current_user, TokenData

router = APIRouter(prefix="/business", tags=["business"])

# ---------------- Candidates ----------------
@router.get("/candidates", response_model=List[Candidate])
def list_candidates(current_user: TokenData = Depends(get_current_user)):
    return crud.list_candidates(current_user)

# ---------------- Centres ----------------
@router.get("/centres", response_model=List[Centre])
def list_centres(current_user: TokenData = Depends(get_current_user)):
    return crud.list_centres(current_user)

# ---------------- Courses ----------------
@router.get("/courses", response_model=List[Course])
def list_courses(current_user: TokenData = Depends(get_current_user)):
    return crud.list_courses(current_user)

@router.post("/courses", response_model=Course)
def create_course(course: CourseCreate, current_user: TokenData = Depends(get_current_user)):
    return crud.create_course(course, current_user)

# ---------------- Certificates ----------------
@router.get("/certificates", response_model=List[Certificate])
def list_certificates(current_user: TokenData = Depends(get_current_user)):
    return crud.list_certificates(current_user)

@router.post("/certificates", response_model=Certificate)
def create_certificate(cert: CertificateCreate, current_user: TokenData = Depends(get_current_user)):
    return crud.create_certificate(cert, current_user)

# ---------------- Cohorts ----------------
@router.get("/cohorts", response_model=List[Cohort])
def list_cohorts(current_user: TokenData = Depends(get_current_user)):
    return crud.list_cohorts(current_user)

# ---------------- Users ----------------
@router.get("/users", response_model=List[User])
def list_users(current_user: TokenData = Depends(get_current_user)):
    return crud.list_users(current_user)

# ---------------- Course Registrations ----------------
@router.get("/registrations", response_model=List[CourseRegistration])
def list_registrations(current_user: TokenData = Depends(get_current_user)):
    return crud.list_registrations(current_user)

# ---------------- Issued Certificates ----------------
@router.get("/issued-certificates", response_model=List[IssuedCertificate])
def list_issued_certificates(current_user: TokenData = Depends(get_current_user)):
    return crud.list_issued_certificates(current_user)
