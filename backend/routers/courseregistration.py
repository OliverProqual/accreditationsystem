from fastapi import APIRouter
from models.courseregistration import CourseRegistrationCreate, CourseRegistration
import crud.courseregistration as crud

router = APIRouter(prefix="/centres", tags=["centres"])

@router.post("/courseregistrations", response_model=CourseRegistration)
def create_registration(reg: CourseRegistrationCreate):
    return crud.create_registration(reg)


@router.get("/courseregistrations/{registration_id}", response_model=CourseRegistration)
def get_registration(registration_id: int):
    return crud.get_registration(registration_id)


@router.get("/courseregistrations", response_model=list[CourseRegistration])
def list_registrations(limit: int = 10):
    return crud.list_registrations(limit)