from fastapi import APIRouter
from models.cohort import CohortCreate, Cohort
import crud.cohort as crud

router = APIRouter(prefix="/centres", tags=["centres"])

@router.post("/cohorts", response_model=Cohort)
def create_cohort(cohort: CohortCreate):
    return crud.create_cohort(cohort)


@router.get("/cohorts/{cohort_id}", response_model=Cohort)
def get_cohort(cohort_id: int):
    return crud.get_cohort(cohort_id)


@router.get("/cohorts", response_model=list[Cohort])
def list_cohorts(limit: int = 10):
    return crud.list_cohorts(limit)
    
@router.put("/cohorts/{cohort_id}", response_model=Cohort)
def update_cohort(cohort_id: int, cohort: CohortCreate):
    return crud.update_cohort(cohort_id, cohort)


@router.delete("/cohorts/{cohort_id}")
def delete_cohort(cohort_id: int):
    return crud.delete_cohort(cohort_id)