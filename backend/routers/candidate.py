from fastapi import APIRouter
from models.candidate import CandidateCreate, Candidate
import crud.candidate as crud
from typing import List

router = APIRouter(prefix="/centres", tags=["centres"])

@router.get("/candidates", response_model=List[Candidate])
def list_candidates():
    return crud.list_candidates()

@router.get("/candidates/{candidate_id}", response_model=Candidate)
def get_candidate(candidate_id: int):
    return crud.get_candidate(candidate_id)

@router.post("/candidates", response_model=Candidate)
def create_candidate(candidate: Candidate):
    return crud.create_candidate(candidate)


@router.put("/candidates/{candidate_id}", response_model=Candidate)
def update_candidate(candidate_id: int, candidate: CandidateCreate):
    return crud.update_candidate(candidate_id, candidate)


@router.delete("/candidates/{candidate_id}")
def delete_candidate(candidate_id: int):
    return crud.delete_candidate(candidate_id)
