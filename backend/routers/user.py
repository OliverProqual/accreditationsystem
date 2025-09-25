from fastapi import APIRouter
from models.user import UserCreate, User
import crud.user as crud

router = APIRouter(prefix="/centres", tags=["centres"])

@router.post("/users", response_model=User)
def create_user(user: UserCreate):
    return crud.create_user(user)


@router.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    return crud.get_user(user_id)


@router.get("/users", response_model=list[User])
def list_users(limit: int = 10):
    return crud.list_users(limit)
    
@router.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user: UserCreate):
    return crud.update_user(user_id, user)


@router.delete("/users/{user_id}")
def delete_user(user_id: int):
    return crud.delete_user(user_id)
