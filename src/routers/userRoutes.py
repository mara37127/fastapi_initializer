from services.authService import AuthService
from schemas import  User
from fastapi import  HTTPException, APIRouter, Depends
from fastapi.security import  HTTPBearer
from dependencies import get_db, isAuthenticated
from typing import List
import logging

from services.userService import UserService

# get root logger
logger = logging.getLogger(__name__)


router = APIRouter(
    prefix='/users',
    tags=['users'],
    dependencies=[Depends(isAuthenticated)],
    responses={404: {"description": "Not found"}}
)

security = HTTPBearer()
auth_handler = AuthService()
user_service = UserService()


@router.get("/", response_model=List[User])
def read_users(skip: int = 0, limit: int = 100):
    logger.info("---getting users---")
    users = user_service.get_users(skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=User)
def read_user(user_id: int):
    logger.info(f"---getting user {user_id}---")
    db_user = user_service.get_user(user_id=user_id)
    if db_user is None:
        logger.exception(f"user {user_id} not found")
        raise HTTPException(status_code=404, detail="User not found")
    return db_user