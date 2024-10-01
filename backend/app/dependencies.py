from fastapi import Depends
from .database import Database
from fastapi import Depends, HTTPException, status

from . import auth, schemas


def get_db():
    with Database() as db:
        yield db

def require_role(required_role: str):
    def role_checker(current_user: schemas.User = Depends(auth.get_current_user)):
        if current_user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted",
            )
        return current_user
    return role_checker
