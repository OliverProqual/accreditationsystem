from fastapi import APIRouter
from models.course import CourseCreate, Course
import crud.course as crud

router = APIRouter(prefix="/centres", tags=["centres"])

@router.post("/courses", response_model=Course)
def create_course(course: CourseCreate):
    return crud.create_course(course)


@router.get("/courses/{course_id}", response_model=Course)
def get_course(course_id: int):
    return crud.get_course(course_id)


@router.get("/courses", response_model=list[Course])
def list_courses(limit: int = 10):
    return crud.list_courses(limit)
    
@router.put("/courses/{course_id}", response_model=Course)
def update_course(course_id: int, course: CourseCreate):
    return crud.update_course(course_id, course)


# ---- Delete course ----
@router.delete("/courses/{course_id}")
def delete_course(course_id: int):
    return crud.delete_course(course_id)