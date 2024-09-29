import logging
from fastapi import APIRouter, HTTPException, Depends
from .. import schemas, database, auth
from typing import List

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/scores",
    tags=["scores"],
)

@router.post("/", response_model=schemas.Score)
def create_new_score(score: schemas.ScoreCreate, current_user: schemas.User = Depends(auth.get_current_user)):
    logger.info(f"User {current_user.user_id} is creating a new score with details: {score}")
    
    db = database.Database()
    try:
        new_score = db.create_score(score=score, user_id=current_user.user_id)
        logger.info(f"New score created with id={new_score.id} by user {current_user.user_id}")
        return new_score
    except Exception as e:
        logger.error(f"Error creating new score for user {current_user.user_id}: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while creating the score")
    finally:
        db.close()

@router.get("/my-scores", response_model=List[schemas.Score])
def read_user_scores(current_user: schemas.User = Depends(auth.get_current_user)):
    logger.info(f"Fetching scores for user {current_user.user_id}")
    
    db = database.Database()
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
    finally:
        db.close()

@router.get("/section/{section_id}", response_model=List[schemas.Score])
def read_section_scores(section_id: int):
    logger.info(f"Fetching scores for section_id={section_id}")
    
    db = database.Database()
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
    finally:
        db.close()
