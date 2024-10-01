import logging
from fastapi import APIRouter, HTTPException, Depends
from .. import schemas, database, auth, dependencies
from typing import List

# Set up logging
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/scores",
    tags=["scores"],
)

@router.post("/", response_model=schemas.ScoreOut)
def create_new_score(
    score: schemas.ScoreCreate, 
    current_user: schemas.User = Depends(auth.get_current_user),
    db: database.Database = Depends(dependencies.get_db)
):
    logger.info(f"User {current_user.user_id} is creating a new score with details: {score}")
    
    try:
        new_score = db.create_score(score=score, user_id=current_user.user_id)
        logger.info(f"New score created with id={new_score.id} by user {current_user.user_id}")
        return new_score
    except Exception as e:
        logger.error(f"Error creating new score for user {current_user.user_id}: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while creating the score")

@router.get("/my-scores", response_model=List[schemas.ScoreOut])
def read_user_scores(
    current_user: schemas.User = Depends(auth.get_current_user),
    db: database.Database = Depends(dependencies.get_db)
):
    logger.info(f"Fetching scores for user {current_user.user_id}")
    
    try:
        scores = db.get_user_scores(user_id=current_user.user_id)
        if not scores:
            logger.warning(f"No scores found for user {current_user.user_id}")
            raise HTTPException(status_code=404, detail="No scores found for this user")
        logger.info(f"Found {len(scores)} scores for user {current_user.user_id}")
        return scores
    except Exception as e:
        logger.error(f"Error fetching scores for user {current_user.user_id}: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while fetching the scores")

@router.get("/section/{section_id}", response_model=List[schemas.ScoreOut])
def read_section_scores(
    section_id: int,
    db: database.Database = Depends(dependencies.get_db)
):
    logger.info(f"Fetching scores for section_id={section_id}")
    
    try:
        scores = db.get_section_scores(section_id=section_id)
        if not scores:
            logger.warning(f"No scores found for section_id={section_id}")
            raise HTTPException(status_code=404, detail="No scores found for this section")
        logger.info(f"Found {len(scores)} scores for section_id={section_id}")
        return scores
    except Exception as e:
        logger.error(f"Error fetching scores for section_id={section_id}: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while fetching the scores")



@router.get("/attempts", response_model=int)
def get_attempt_number(
    section_id: int,
    current_user: schemas.User = Depends(auth.get_current_user),
    db: database.Database = Depends(dependencies.get_db)
):
    """
    Fetch the current attempt number for the section and user.
    """
    logger.info(f"Fetching attempt count for user {current_user.user_id} and section_id={section_id}")
    
    try:
        # Fetch attempts made by the user for the given section
        attempts_count = db.get_user_section_attempts_count(user_id=current_user.user_id, section_id=section_id)
        
        # If no attempts found, default to 0
        if attempts_count is None:
            logger.warning(f"No attempts found for user {current_user.user_id} in section_id={section_id}")
            attempts_count = 0
        
        logger.info(f"User {current_user.user_id} has made {attempts_count} attempts for section_id={section_id}")
        return attempts_count
    except Exception as e:
        logger.error(f"Error fetching attempts for user {current_user.user_id} and section_id={section_id}: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while fetching the attempt count")
