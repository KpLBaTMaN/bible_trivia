# database.py
import os
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker, Session
from . import models, schemas, auth
from typing import List, Optional

DATABASE_URL = os.getenv(
    'DATABASE_URL',
    'mysql+pymysql://your_db_user:your_db_password@db:3306/bible_trivia_db'
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Database:
    def __init__(self):
        self.db: Session = SessionLocal()

    def close(self):
        self.db.close()
        
        
    # ---------------- User Methods ----------------

    def get_user(self, user_id: int):
        return self.db.query(models.User).filter(models.User.user_id == user_id).first()

    def get_user_by_username(self, username: str):
        return self.db.query(models.User).filter(models.User.username == username).first()

    def create_user(self, user: schemas.UserCreate, role: schemas.Role = schemas.Role.user):
        # Hash the user's password
        hashed_password = auth.get_password_hash(user.password)
        
        # Create the User model instance, setting the role internally
        db_user = models.User(
            username=user.username,
            email=user.email,
            password_hash=hashed_password,
            role=role  # Set role from argument, default is Role.user
        )
        
        # Add and commit the new user to the database
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        
        return db_user
    
    
    # ---------------- Section Methods ----------------

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

    # ---------------- Question Methods ----------------

    def get_questions_by_section(
        self, 
        section_id: int, 
        difficulty: Optional[str] = None
    ) -> List[models.Question]:
        """Retrieve questions by section with optional difficulty filtering."""
        query = self.db.query(models.Question).filter(models.Question.section_id == section_id)
        if difficulty:
            query = query.filter(models.Question.difficulty == difficulty)
        return query.all()

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
    
    def get_question(self, question_id: int) -> Optional[models.Question]:
        """Retrieve a question by its ID."""
        return self.db.query(models.Question).filter(models.Question.question_id == question_id).first()

    def get_all_questions(self) -> List[models.Question]:
        """Retrieve all questions in the database."""
        return self.db.query(models.Question).all()
    
    
    # ---------------- Score Methods ----------------

    def create_score(self, score: schemas.ScoreCreate, user_id: int):
        """Create a new score entry for a user."""
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

    def get_user_scores(self, user_id: int) -> List[models.Score]:
        """Retrieve all scores for a specific user."""
        return self.db.query(models.Score).filter(models.Score.user_id == user_id).all()

    def get_section_scores(self, section_id: int) -> List[models.Score]:
        """Retrieve all scores for a specific section."""
        return self.db.query(models.Score).filter(models.Score.section_id == section_id).all()

    def get_user_section_attempts_count(self, user_id: int, section_id: int) -> int:
        """
        Get the number of attempts made by the user for the given section based on the highest attempt_number.
        """
        # Query the maximum attempt_number for the user and section
        max_attempt = self.db.query(func.max(models.Score.attempt_number)).filter(
            models.Score.user_id == user_id,
            models.Score.section_id == section_id
        ).scalar()
        
        print("MAX!!: ", max_attempt)

        # If no attempts are found, return 0; otherwise return the max_attempt
        return max_attempt if max_attempt is not None else 0

    
    # ---------------- Bible Verse Methods ----------------

    def get_bible_verse(self, book_name: str, chapter: int, verse: int):
        """Retrieve a specific Bible verse by book name, chapter, and verse."""
        return self.db.query(models.BibleVerse).filter(
            models.BibleVerse.book_name == book_name,
            models.BibleVerse.chapter == chapter,
            models.BibleVerse.verse == verse
        ).first()

    def create_bible_verse(self, verse: schemas.BibleVerseCreate):
        """Create a new Bible verse entry."""
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
    
    def get_bible_verses_for_section(self, section_id: int) -> List[str]:
        """Retrieve all Bible verses associated with a specific section."""
        # Assuming each question in a section has a bible_text or bible_reference
        questions = self.db.query(models.Question).filter(models.Question.section_id == section_id).all()
        bible_verses = list({q.bible_text for q in questions if q.bible_text})
        return bible_verses
    
    def get_bible_verse_by_details(self, book_name: str, chapter: int, verse: int, version: str):
        """Retrieve a specific Bible verse by book name, chapter, verse, and version."""
        return self.db.query(models.BibleVerse).filter(
            models.BibleVerse.book_name == book_name,
            models.BibleVerse.chapter == chapter,
            models.BibleVerse.verse == verse,
            models.BibleVerse.version == version
        ).first()

    def get_bible_verse_by_id(self, verse_id: int):
        """Retrieve a Bible verse by its unique ID."""
        return self.db.query(models.BibleVerse).filter(models.BibleVerse.verse_id == verse_id).first()

    def get_bible_verses(self, skip: int = 0, limit: int = 100) -> List[models.BibleVerse]:
        """Retrieve a list of Bible verses with pagination."""
        return self.db.query(models.BibleVerse).offset(skip).limit(limit).all()

    def update_bible_verse(self, verse_id: int, verse_update: schemas.BibleVerseCreate):
        """Update an existing Bible verse."""
        db_verse = self.get_bible_verse_by_id(verse_id)
        if not db_verse:
            return None
        for key, value in verse_update.dict().items():
            setattr(db_verse, key, value)
        self.db.commit()
        self.db.refresh(db_verse)
        return db_verse

    def delete_bible_verse(self, verse_id: int):
        """Delete a Bible verse by its ID."""
        db_verse = self.get_bible_verse_by_id(verse_id)
        if not db_verse:
            return False
        self.db.delete(db_verse)
        self.db.commit()
        return True
    
    # ---------------- Progress Methods ----------------

    def create_progress(self, progress: schemas.ProgressCreate) -> schemas.Progress:
        """
        Create a new progress record in the database.

        :param progress: ProgressCreate schema containing progress details.
        :return: Progress schema with the newly created progress.
        """
        
        db_progress = models.Progress(
            user_id=progress.user_id,
            section_id=progress.section_id,
            question_id=progress.question_id,
            is_correct=progress.is_correct,
            is_unsure=progress.is_unsure
        )
        self.db.add(db_progress)
        self.db.commit()
        self.db.refresh(db_progress)
        return db_progress
    
    
    def create_progress_entries(self, progress_list: List[schemas.ProgressCreate]) -> List[models.Progress]:
        """
        Bulk create progress records in the database.

        :param progress_list: List of ProgressCreate schemas containing progress details.
        :return: List of Progress model instances with the newly created progresses.
        """
        db_progresses = [
            models.Progress(
                user_id=progress.user_id,
                section_id=progress.section_id,
                question_id=progress.question_id,
                is_correct=progress.is_correct,
                is_unsure=progress.is_unsure,
                score_id=progress.score_id  # Assign score_id
            ) for progress in progress_list
        ]
        self.db.bulk_save_objects(db_progresses)
        self.db.commit()
        for progress in db_progresses:
            self.db.refresh(progress)
        return db_progresses

    def get_user_progress(self, user_id: int) -> List[models.Progress]:
        """
        Retrieve all progress records for a specific user.

        :param user_id: The ID of the user.
        :return: A list of Progress model instances.
        """
        progresses = self.db.query(models.Progress).filter(models.Progress.user_id == user_id).all()
        return progresses
    
    # ---------------- Leaderboard Methods ----------------

    def get_global_leaderboard(self, top_n: int = 10) -> List[schemas.UserScore]:
        """
        Retrieve the top N users based on total scores across all sections.

        :param top_n: Number of top users to retrieve.
        :return: List of UserScore schemas.
        """
        # Sum the scores per user
        results = self.db.query(
            models.User.username,
            func.sum(models.Score.score).label('total_score')
        ).join(
            models.Score, models.User.user_id == models.Score.user_id
        ).group_by(
            models.User.user_id
        ).order_by(
            func.sum(models.Score.score).desc()
        ).limit(top_n).all()

        # Convert the results into UserScore schemas
        leaderboard = [
            schemas.UserScore(username=username, total_score=total_score) 
            for username, total_score in results
        ]
        return leaderboard

    def get_section_leaderboard(self, section_id: int, top_n: int = 10) -> List[schemas.UserScore]:
        """
        Retrieve the top N users based on total scores for a specific section.

        :param section_id: The ID of the section.
        :param top_n: Number of top users to retrieve.
        :return: List of UserScore schemas.
        """
        results = self.db.query(
            models.User.username,
            func.sum(models.Score.score).label('total_score')
        ).join(
            models.Score, models.User.user_id == models.Score.user_id
        ).filter(
            models.Score.section_id == section_id
        ).group_by(
            models.User.user_id
        ).order_by(
            func.sum(models.Score.score).desc()
        ).limit(top_n).all()

        # Convert the results into UserScore schemas
        leaderboard = [
            schemas.UserScore(username=username, total_score=total_score)
            for username, total_score in results
        ]
        return leaderboard
    

    # ---------------- Context Manager Support ----------------

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
