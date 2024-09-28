import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud, database
from typing import List

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/sections",
    tags=["sections"],
)

@router.get("/", response_model=List[schemas.Section])
def read_sections(db: Session = Depends(database.SessionLocal)):
    logger.info("Fetching all sections")
    
    try:
        sections = crud.get_sections(db)
        if not sections:
            logger.warning("No sections found")
            raise HTTPException(status_code=404, detail="No sections found")
        
        logger.info(f"Found {len(sections)} sections")
        return sections
    except Exception as e:
        logger.error(f"Error fetching sections: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while fetching sections")

@router.post("/", response_model=schemas.Section)
def create_new_section(section: schemas.SectionCreate, db: Session = Depends(database.SessionLocal)):
    logger.info(f"Creating a new section with details: {section}")
    
    try:
        new_section = crud.create_section(db=db, section=section)
        logger.info(f"Created new section with id={new_section.id}")
        return new_section
    except Exception as e:
        logger.error(f"Error creating new section: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while creating the section")

@router.get("/{section_id}", response_model=schemas.Section)
def read_section(section_id: int, db: Session = Depends(database.SessionLocal)):
    logger.info(f"Fetching section with id={section_id}")
    
    try:
        section = crud.get_section(db, section_id=section_id)
        if section is None:
            logger.warning(f"Section not found with id={section_id}")
            raise HTTPException(status_code=404, detail="Section not found")
        
        logger.info(f"Found section with id={section_id}")
        return section
    except Exception as e:
        logger.error(f"Error fetching section with id={section_id}: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while fetching the section")
