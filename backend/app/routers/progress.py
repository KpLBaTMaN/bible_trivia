# app/routers/progress.py
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from .. import schemas, dependencies, auth, database
import logging

router = APIRouter(
    prefix="/progress",
    tags=["progress"],
)

logger = logging.getLogger(__name__)

@router.post("/", response_model=schemas.Progress)
def create_progress(progress: schemas.ProgressCreate, current_user: schemas.User = Depends(auth.get_current_user), db: database.Database = Depends(dependencies.get_db)):
    logger.info(f"User {current_user.user_id} is creating progress for question {progress.question_id} in section {progress.section_id}")
    
    try:
        new_progress = db.create_progress(progress=progress)
        logger.info(f"Progress created with id={new_progress.id} for user {current_user.user_id}")
        return new_progress
    except Exception as e:
        logger.error(f"Error creating progress for user {current_user.user_id}: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while creating progress")
        
@router.get("/my-progress", response_model=List[schemas.Progress])
def read_user_progress(current_user: schemas.User = Depends(auth.get_current_user), db: database.Database = Depends(dependencies.get_db)):
    logger.info(f"Fetching progress for user {current_user.user_id}")
    
    progress = db.get_user_progress(user_id=current_user.user_id)
    if not progress:
        logger.warning(f"No progress found for user {current_user.user_id}")
        raise HTTPException(status_code=404, detail="No progress found for this user")
    
    logger.info(f"Found {len(progress)} progress records for user {current_user.user_id}")
    return progress