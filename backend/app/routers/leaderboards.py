# app/routers/leaderboard.py
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from .. import schemas, dependencies, auth, database
import logging

router = APIRouter(
    prefix="/leaderboard",
    tags=["leaderboard"],
)

logger = logging.getLogger(__name__)

@router.get("/global", response_model=List[schemas.UserScore])
def get_global_leaderboard(db: database.Database = Depends(dependencies.get_db)):
    logger.info("Fetching global leaderboard")
    
    leaderboard = db.get_global_leaderboard()
    if not leaderboard:
        logger.warning("No leaderboard data found")
        raise HTTPException(status_code=404, detail="No leaderboard data found")
    
    return leaderboard

@router.get("/section/{section_id}", response_model=List[schemas.UserScore])
def get_section_leaderboard(section_id: int, db: database.Database = Depends(dependencies.get_db)):
    logger.info(f"Fetching leaderboard for section_id={section_id}")
    
    leaderboard = db.get_section_leaderboard(section_id=section_id)
    if not leaderboard:
        logger.warning(f"No leaderboard data found for section_id={section_id}")
        raise HTTPException(status_code=404, detail="No leaderboard data found for this section")
    
    return leaderboard
