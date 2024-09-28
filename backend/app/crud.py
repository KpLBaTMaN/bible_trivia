from sqlalchemy.orm import Session
from . import models, schemas, auth

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.user_id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_sections(db: Session):
    return db.query(models.Section).all()

def get_section(db: Session, section_id: int):
    return db.query(models.Section).filter(models.Section.section_id == section_id).first()

def create_section(db: Session, section: schemas.SectionCreate):
    db_section = models.Section(
        name=section.name,
        description=section.description
    )
    db.add(db_section)
    db.commit()
    db.refresh(db_section)
    return db_section

def get_questions_by_section(db: Session, section_id: int):
    return db.query(models.Question).filter(models.Question.section_id == section_id).all()

def create_question(db: Session, question: schemas.QuestionCreate):
    db_question = models.Question(
        section_id=question.section_id,
        question_text=question.question_text,
        option1=question.option1,
        option2=question.option2,
        option3=question.option3,
        option4=question.option4,
        correct_option=question.correct_option,
        bible_reference=question.bible_reference,
        bible_text=question.bible_text,
        difficulty=question.difficulty,  # Now required
        topic=question.topic,  # Now required
        tags=question.tags,  # JSON field
        hint=question.hint,
        bible_reference_book=question.bible_reference_book,
        bible_reference_start_chapter=question.bible_reference_start_chapter,
        bible_reference_end_chapter=question.bible_reference_end_chapter,
        bible_reference_start_verse=question.bible_reference_start_verse,
        bible_reference_end_verse=question.bible_reference_end_verse
    )
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

def create_score(db: Session, score: schemas.ScoreCreate, user_id: int):
    db_score = models.Score(
        user_id=user_id,
        section_id=score.section_id,
        attempt_number=score.attempt_number,
        score=score.score,
        time_taken=score.time_taken
    )
    db.add(db_score)
    db.commit()
    db.refresh(db_score)
    return db_score

def get_user_scores(db: Session, user_id: int):
    return db.query(models.Score).filter(models.Score.user_id == user_id).all()

def get_bible_verse(db: Session, book_name: str, chapter: int, verse: int):
    """Retrieve a specific Bible verse by book name, chapter, and verse."""
    return db.query(models.BibleVerse).filter(
        models.BibleVerse.book_name == book_name,
        models.BibleVerse.chapter == chapter,
        models.BibleVerse.verse == verse
    ).first()

def create_bible_verse(db: Session, verse: schemas.BibleVerseCreate):
    db_verse = models.BibleVerse(
        book_name=verse.book_name,
        chapter=verse.chapter,
        verse=verse.verse,
        text=verse.text,
        version=verse.version
    )
    db.add(db_verse)
    db.commit()
    db.refresh(db_verse)
    return db_verse

def get_question(db: Session, question_id: int):
    """Retrieve a question by its ID."""
    return db.query(models.Question).filter(models.Question.question_id == question_id).first()

 
#### REMOVE THERE IS NO LONGER (schemas.QuestionUpdate)
# def update_question(db: Session, question_id: int, question_update: schemas.QuestionUpdate):
#     """Update an existing question."""
#     db_question = get_question(db, question_id)
#     if db_question:
#         for key, value in question_update.dict().items():
#             if value is not None:
#                 setattr(db_question, key, value)
#         db.commit()
#         db.refresh(db_question)
#     return db_question

def get_all_questions(db: Session):
    """Retrieve all questions in the database."""
    return db.query(models.Question).all()

def get_section_scores(db: Session, section_id: int):
    """Retrieve all scores for a specific section."""
    return db.query(models.Score).filter(models.Score.section_id == section_id).all()

