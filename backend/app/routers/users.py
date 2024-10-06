#users.py
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from typing import Optional
from fastapi import status

from .. import schemas, auth, database, dependencies
from ..enums import Role

# Set up logging
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.post("/register", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def register_user(
    user: schemas.UserCreate, 
    db: database.Database = Depends(dependencies.get_db)
):
    logger.info(f"Attempting to register new user: {user.username}")
    
    try:
        db_user = db.get_user_by_username(username=user.username)
        if db_user:
            logger.warning(f"Registration failed: Username {user.username} is already registered")
            raise HTTPException(status_code=400, detail="Username already registered")
        
        new_user = db.create_user(
            user=schemas.UserCreate(
                username=user.username, 
                password=user.password
            ),
            role=Role.user
        )
        
        logger.info(f"Successfully registered user with username: {user.username}")
        return new_user
    except Exception as e:
        logger.error(f"Error registering user {user.username}: {e}")
        raise HTTPException(status_code=500, detail="An error occurred during user registration")


@router.post("/login")
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: database.Database = Depends(dependencies.get_db)
):
    logger.info(f"Login attempt for username: {form_data.username}")
    
    try:
        user = db.get_user_by_username(username=form_data.username)
 
        if not user or not auth.verify_password(form_data.password, user.password_hash):
            logger.warning(f"Login failed for username: {form_data.username} - Incorrect username or password")
            raise HTTPException(status_code=400, detail="Incorrect username or password")
        
        access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = auth.create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        logger.info(f"User {form_data.username} successfully logged in")
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        logger.error(f"Error during login for username {form_data.username}: {e}")
        raise HTTPException(status_code=500, detail="An error occurred during login")


@router.get("/me", response_model=schemas.User)
def get_current_user_profile(
    current_user: schemas.User = Depends(auth.get_current_user)
):
    logger.info(f"Retrieving profile for current user: {current_user.username}")
    return current_user
