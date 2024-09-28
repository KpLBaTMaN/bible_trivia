import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud, database, auth
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from typing import List

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/scores",
    tags=["scores"],
)

@router.post("/", response_model=schemas.Score)
def create_new_score(score: schemas.ScoreCreate, db: Session = Depends(database.SessionLocal), current_user: schemas.User = Depends(auth.get_current_user)):
    logger.info(f"User {current_user.user_id} is creating a new score with details: {score}")
    
    try:
        new_score = crud.create_score(db=db, score=score, user_id=current_user.user_id)
        logger.info(f"New score created with id={new_score.id} by user {current_user.user_id}")
        return new_score
    except Exception as e:
        logger.error(f"Error creating new score for user {current_user.user_id}: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while creating the score")

@router.get("/my-scores", response_model=List[schemas.Score])
def read_user_scores(db: Session = Depends(database.SessionLocal), current_user: schemas.User = Depends(auth.get_current_user)):
    logger.info(f"Fetching scores for user {current_user.user_id}")
    
    try:
        scores = crud.get_user_scores(db, user_id=current_user.user_id)
        if not scores:
            logger.warning(f"No scores found for user {current_user.user_id}")
            raise HTTPException(status_code=404, detail="No scores found for this user")
        logger.info(f"Found {len(scores)} scores for user {current_user.user_id}")
        return scores
    except Exception as e:
        logger.error(f"Error fetching scores for user {current_user.user_id}: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while fetching the scores")

@router.get("/section/{section_id}", response_model=List[schemas.Score])
def read_section_scores(section_id: int, db: Session = Depends(database.SessionLocal)):
    logger.info(f"Fetching scores for section_id={section_id}")
    
    try:
        scores = crud.get_section_scores(db, section_id=section_id)
        if not scores:
            logger.warning(f"No scores found for section_id={section_id}")
            raise HTTPException(status_code=404, detail="No scores found for this section")
        logger.info(f"Found {len(scores)} scores for section_id={section_id}")
        return scores
    except Exception as e:
        logger.error(f"Error fetching scores for section_id={section_id}: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while fetching the scores")
