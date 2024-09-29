# database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from . import models, schemas, auth

DATABASE_URL = os.getenv(
    'DATABASE_URL',
    'mysql+pymysql://your_db_user:your_db_password@db:3306/bible_trivia_db'
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Database:
    def __init__(self):
        self.db: Session = SessionLocal()

    def close(self):
        self.db.close()

    def get_user(self, user_id: int):
        return self.db.query(models.User).filter(models.User.user_id == user_id).first()

    def get_user_by_username(self, username: str):
        return self.db.query(models.User).filter(models.User.username == username).first()

    def create_user(self, user: schemas.UserCreate):
        hashed_password = auth.get_password_hash(user.password)
        db_user = models.User(
            username=user.username,
            email=user.email,
            password_hash=hashed_password
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_sections(self):
        return self.db.query(models.Section).all()

    def get_section(self, section_id: int):
        return self.db.query(models.Section).filter(models.Section.section_id == section_id).first()

    def create_section(self, section: schemas.SectionCreate):
        db_section = models.Section(
            name=section.name,
            description=section.description
        )
        self.db.add(db_section)
        self.db.commit()
        self.db.refresh(db_section)
        return db_section

    def get_questions_by_section(self, section_id: int):
        return self.db.query(models.Question).filter(models.Question.section_id == section_id).all()

    def create_question(self, question: schemas.QuestionCreate):
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
        self.db.add(db_question)
        self.db.commit()
        self.db.refresh(db_question)
        return db_question

    def create_score(self, score: schemas.ScoreCreate, user_id: int):
        db_score = models.Score(
            user_id=user_id,
            section_id=score.section_id,
            attempt_number=score.attempt_number,
            score=score.score,
            time_taken=score.time_taken
        )
        self.db.add(db_score)
        self.db.commit()
        self.db.refresh(db_score)
        return db_score

    def get_user_scores(self, user_id: int):
        return self.db.query(models.Score).filter(models.Score.user_id == user_id).all()

    def get_bible_verse(self, book_name: str, chapter: int, verse: int):
        """Retrieve a specific Bible verse by book name, chapter, and verse."""
        return self.db.query(models.BibleVerse).filter(
            models.BibleVerse.book_name == book_name,
            models.BibleVerse.chapter == chapter,
            models.BibleVerse.verse == verse
        ).first()

    def create_bible_verse(self, verse: schemas.BibleVerseCreate):
        db_verse = models.BibleVerse(
            book_name=verse.book_name,
            chapter=verse.chapter,
            verse=verse.verse,
            text=verse.text,
            version=verse.version
        )
        self.db.add(db_verse)
        self.db.commit()
        self.db.refresh(db_verse)
        return db_verse

    def get_question(self, question_id: int):
        """Retrieve a question by its ID."""
        return self.db.query(models.Question).filter(models.Question.question_id == question_id).first()

    def get_all_questions(self):
        """Retrieve all questions in the database."""
        return self.db.query(models.Question).all()

    def get_section_scores(self, section_id: int):
        """Retrieve all scores for a specific section."""
        return self.db.query(models.Score).filter(models.Score.section_id == section_id).all()
