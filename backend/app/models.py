from sqlalchemy import Column, Integer, String, ForeignKey, Text, Enum as SqlEnum, Table
from sqlalchemy.orm import relationship
from sqlalchemy.types import JSON
from typing import List

from app.database import Base
from app.enums import Tag, Difficulty, Topics, BibleBook

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    total_score = Column(Integer, default=0)

    scores = relationship('Score', back_populates='user')

class Section(Base):
    __tablename__ = 'sections'
    section_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)

    questions = relationship('Question', back_populates='section')

class Question(Base):
    __tablename__ = 'questions'
    question_id = Column(Integer, primary_key=True, index=True)
    section_id = Column(Integer, ForeignKey('sections.section_id'), nullable=False)
    question_text = Column(String(500), nullable=False)
    option1 = Column(String(255), nullable=False)
    option2 = Column(String(255), nullable=False)
    option3 = Column(String(255), nullable=False)
    option4 = Column(String(255), nullable=False)
    correct_option = Column(Integer, nullable=False)
    bible_reference = Column(String(100), nullable=False)
    bible_text = Column(String(1000), nullable=True)
    difficulty = Column(SqlEnum(Difficulty), nullable=False)  # Use SQLAlchemy Enum for Difficulty
    tags = Column(JSON, nullable=True)  # Store tags as a JSON array for flexibility
    topic = Column(SqlEnum(Topics), nullable=True)  # Use SQLAlchemy Enum for Topic
    hint = Column(String(500), nullable=True)
    bible_reference_book = Column(SqlEnum(BibleBook), nullable=True)
    bible_reference_start_chapter = Column(Integer, nullable=True)
    bible_reference_end_chapter = Column(Integer, nullable=True)
    bible_reference_start_verse = Column(Integer, nullable=True)
    bible_reference_end_verse = Column(Integer, nullable=True)

    section = relationship('Section', back_populates='questions')
    
    def get_tags(self) -> List[Tag]:
        """Convert stored JSON list of tag strings to a list of Tag enums."""
        if self.tags:
            return [Tag(tag) for tag in self.tags]
        return []

    def set_tags(self, tag_list: List[Tag]):
        """Set tags from a list of Tag enums by converting them to strings."""
        self.tags = [tag.value for tag in tag_list]

class Score(Base):
    __tablename__ = 'scores'
    score_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    section_id = Column(Integer, ForeignKey('sections.section_id'), nullable=False)
    attempt_number = Column(Integer, nullable=False)
    score = Column(Integer, nullable=False)
    time_taken = Column(Integer, nullable=False)

    user = relationship('User', back_populates='scores')
    section = relationship('Section')

class BibleVerse(Base):
    __tablename__ = 'bible_verses'
    id = Column(Integer, primary_key=True, index=True)
    book_name = Column(String(100), nullable=False)
    chapter = Column(Integer, nullable=False)
    verse = Column(Integer, nullable=False)
    text = Column(String(2000), nullable=False)  # Adjust the length as needed
    version = Column(String(50), default="KJV", nullable=False)