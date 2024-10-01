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
logger.setLevel(logging.DEBUG)  # Capture all levels of logs

@router.post("/", response_model=List[schemas.Progress])
def create_progress(
    progress_list: List[schemas.ProgressCreate],
    current_user: schemas.User = Depends(auth.get_current_user),
    db: database.Database = Depends(dependencies.get_db)
):
    logger.info(f"User {current_user.user_id} is creating progress for multiple questions")
    
    # Assign user_id to each progress entry
    for progress in progress_list:
        progress.user_id = current_user.user_id
    
    try:
        new_progress_list = db.create_progress_entries(progress_list=progress_list)
        logger.info(f"Progress created for user {current_user.user_id}")
        return new_progress_list
    except Exception as e:
        logger.error(f"Error creating progress for user {current_user.user_id}: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while creating progress")

@router.get("/my-progress", response_model=List[schemas.Progress])
def read_user_progress(
    current_user: schemas.User = Depends(auth.get_current_user),
    db: database.Database = Depends(dependencies.get_db)
):
    logger.info(f"Fetching progress for user {current_user.user_id}")
    
    progress = db.get_user_progress(user_id=current_user.user_id)
    if not progress:
        logger.warning(f"No progress found for user {current_user.user_id}")
        raise HTTPException(status_code=404, detail="No progress found for this user")
    
    logger.info(f"Found {len(progress)} progress records for user {current_user.user_id}")
    return progress

@router.post("/submit", response_model=List[schemas.ProgressFeedback])
def submit_progress(
    submission: schemas.ProgressSubmission,
    current_user: schemas.User = Depends(auth.get_current_user),
    db: database.Database = Depends(dependencies.get_db)
):
    logger.info(
        f"User {current_user.user_id} is submitting progress for section {submission.section_id}"
    )

    feedback_list = []
    for question_id, user_answer in submission.answers.items():
        logger.debug(
            f"Processing question_id: {question_id} with user_answer: {user_answer}"
        )

        try:
            # Fetch the correct answer from the database
            question = db.get_question(question_id=question_id)
            if not question:
                logger.warning(
                    f"Question {question_id} not found for user {current_user.user_id}"
                )
                continue

            logger.debug(
                f"Retrieved question: {question.question_text} with correct_option: {question.correct_option}"
            )

            is_correct = user_answer == question.correct_option
            if is_correct:
                logger.info(
                    f"User {current_user.user_id} answered question {question_id} correctly."
                )
            else:
                logger.info(
                    f"User {current_user.user_id} answered question {question_id} incorrectly."
                )

            progress_data = schemas.ProgressCreate(
                user_id=current_user.user_id,
                section_id=submission.section_id,
                question_id=question_id,
                is_correct=is_correct,
                is_unsure=False  # Adjust based on your logic
            )

            # Save progress
            db.create_progress(progress=progress_data)
            logger.debug(
                f"Progress saved for user {current_user.user_id}, question {question_id}"
            )

            # Prepare feedback
            feedback = schemas.ProgressFeedback(
                question_id=question_id,
                question_text=question.question_text,
                user_answer=user_answer,
                correct_answer=question.correct_option,
                result="Correct" if is_correct else "Incorrect",
                explanation=question.hint  # Assuming a hint or explanation field exists
            )
            feedback_list.append(feedback)
            logger.debug(f"Feedback appended for question {question_id}")

        except Exception as e:
            logger.error(
                f"Error processing question {question_id} for user {current_user.user_id}: {e}"
            )
            raise HTTPException(status_code=500, detail="Internal Server Error")

    logger.info(
        f"User {current_user.user_id} submitted progress for section {submission.section_id}"
    )
    logger.debug(f"Feedback list: {feedback_list}")
    return feedback_list
