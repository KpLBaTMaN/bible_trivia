import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud, database
from typing import List

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/questions",
    tags=["questions"],
)

@router.get("/section/{section_id}", response_model=List[schemas.Question])
def read_questions_by_section(section_id: int, db: Session = Depends(database.SessionLocal)):
    logger.info(f"Fetching questions for section_id={section_id}")
    questions = crud.get_questions_by_section(db, section_id=section_id)
    
    if not questions:
        logger.warning(f"No questions found for section_id={section_id}")
        raise HTTPException(status_code=404, detail="No questions found for this section")
    
    logger.info(f"Found {len(questions)} questions for section_id={section_id}")
    return questions

@router.post("/", response_model=schemas.Question)
def create_new_question(question: schemas.QuestionCreate, db: Session = Depends(database.SessionLocal)):
    logger.info(f"Creating a new question with title='{question.title}'")
    new_question = crud.create_question(db=db, question=question)
    logger.info(f"Created new question with id={new_question.id}")
    return new_question

@router.get("/{question_id}", response_model=schemas.Question)
def read_question(question_id: int, db: Session = Depends(database.SessionLocal)):
    logger.info(f"Fetching question with id={question_id}")
    question = crud.get_question(db, question_id=question_id)
    
    if question is None:
        logger.warning(f"Question not found with id={question_id}")
        raise HTTPException(status_code=404, detail="Question not found")
    
    logger.info(f"Found question with id={question_id}")
    return question

@router.get("/", response_model=List[schemas.Question])
def read_all_questions(db: Session = Depends(database.SessionLocal)):
    logger.info("Fetching all questions")
    questions = crud.get_all_questions(db)
    
    if not questions:
        logger.warning("No questions found")
        raise HTTPException(status_code=404, detail="No questions found")
    
    logger.info(f"Found {len(questions)} questions in total")
    return questions
