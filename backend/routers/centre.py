from fastapi import APIRouter
from models.centre import CentreCreate, Centre
import crud.centre as crud

router = APIRouter(prefix="/centres", tags=["centres"])

@router.post("/", response_model=Centre)
def create_centre(centre: CentreCreate):
    return crud.create_centre(centre)

@router.get("/{centre_id}", response_model=Centre)
def read_centre(centre_id: int):
    return crud.get_centre(centre_id)

# add update and delete endpoints similarly
# ---- Update Centre ----
@router.put("/centres/{centre_id}", response_model=Centre)
def update_centre(centre_id: int, centre: CentreCreate):
    return crud.update_centre(centre_id, centre)

# ---- Delete Centre ----
@router.delete("/centres/{centre_id}")
def delete_centre(centre_id: int):
    return crud.delete_centre(centre_id)
