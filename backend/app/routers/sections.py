import logging
from fastapi import APIRouter, HTTPException, Depends
from .. import schemas, database, dependencies, auth
from typing import List

# Set up logging
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/sections",
    tags=["sections"],
)

@router.get("/", response_model=List[schemas.Section])
def read_sections(
    db: database.Database = Depends(dependencies.get_db)
):
    logger.info("Fetching all sections")
    
    try:
        # Fetch all sections
        sections = db.get_sections()  # Assuming it fetches the questions relationship as well
        if not sections:
            logger.warning("No sections found")
            raise HTTPException(status_code=404, detail="No sections found")
        
        logger.info(f"Found {len(sections)} sections")
        
        # Return sections with calculated total_questions
        return [
            schemas.Section(
                section_id=section.section_id,
                name=section.name,
                description=section.description,
                total_questions=len(section.questions)  # Assuming questions are eagerly loaded
            )
            for section in sections
        ]
    except Exception as e:
        logger.error(f"Error fetching sections: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while fetching sections")



@router.post("/", response_model=schemas.Section)
def create_new_section(
    section: schemas.SectionCreate,
    db: database.Database = Depends(dependencies.get_db)
):
    logger.info(f"Creating a new section with details: {section}")
    
    try:
        new_section = db.create_section(section=section)
        logger.info(f"Created new section with id={new_section.id}")
        return new_section
    except Exception as e:
        logger.error(f"Error creating new section: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while creating the section")

@router.get("/{section_id}", response_model=schemas.Section)
def read_section(
    section_id: int,
    db: database.Database = Depends(dependencies.get_db)
):
    logger.info(f"Fetching section with id={section_id}")
    
    try:
        section = db.get_section(section_id=section_id)
        if section is None:
            logger.warning(f"Section not found with id={section_id}")
            raise HTTPException(status_code=404, detail="Section not found")
        
        logger.info(f"Found section with id={section_id}")
        return section
    except Exception as e:
        logger.error(f"Error fetching section with id={section_id}: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while fetching the section")


# app/routers/sections.py
@router.post("/complete", response_model=schemas.SectionCompletionDetail)
def complete_section(completion: schemas.SectionCompletion, current_user: schemas.User = Depends(auth.get_current_user), db: database.Database = Depends(dependencies.get_db)):
    logger.info(f"User {current_user.user_id} completed section {completion.section_id} in {completion.time_taken_seconds} seconds")
    
    bonus = calculate_bonus(completion.time_taken_seconds)
    total_correct, total_incorrect, total_unsure = db.calculate_section_performance(user_id=current_user.user_id, section_id=completion.section_id)
    final_score = total_correct + bonus  # Assuming 1 point per correct answer
    
    bible_verses = db.get_bible_verses_for_section(section_id=completion.section_id)
    
    db.record_section_completion(
        user_id=current_user.user_id,
        section_id=completion.section_id,
        time_taken=completion.time_taken_seconds,
        bonus=bonus,
        total_correct=total_correct,
        total_incorrect=total_incorrect,
        total_unsure=total_unsure
    )
    
    logger.info(f"Section completion recorded for user {current_user.user_id}: correct={total_correct}, incorrect={total_incorrect}, unsure={total_unsure}, bonus={bonus}, final_score={final_score}")
    
    return schemas.SectionCompletionDetail(
        total_correct=total_correct,
        total_incorrect=total_incorrect,
        total_unsure=total_unsure,
        bible_verses=bible_verses,
        final_score=final_score
    )

def calculate_bonus(time_taken_seconds: int) -> int:
    # Define your bonus calculation logic
    if time_taken_seconds < 60:
        return 10
    elif time_taken_seconds < 120:
        return 5
    else:
        return 0
