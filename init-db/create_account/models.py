from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean, Enum as SqlEnum, Table, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.types import JSON
from sqlalchemy.ext.declarative import declarative_base

from typing import List
from datetime import datetime

from create_account.enums import Tag, Difficulty, Topics, BibleBook, Role


Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    role = Column(SqlEnum(Role), default=Role.user)
    
    # Relationships
    scores = relationship("Score", back_populates="user")
    progresses = relationship("Progress", back_populates="user")
    achievements = relationship("Achievement", back_populates="user")


class Section(Base):
    __tablename__ = 'sections'

    section_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    # Relationships
    questions = relationship("Question", back_populates="section")
    scores = relationship("Score", back_populates="section")
    completions = relationship("SectionCompletion", back_populates="section")


class Question(Base):
    __tablename__ = 'questions'

    question_id = Column(Integer, primary_key=True, index=True)
    section_id = Column(Integer, ForeignKey('sections.section_id'), nullable=False)
    question_text = Column(Text, nullable=False)
    option1 = Column(String(255), nullable=False)
    option2 = Column(String(255), nullable=False)
    option3 = Column(String(255), nullable=False)
    option4 = Column(String(255), nullable=False)
    correct_option = Column(Integer, nullable=False)
    bible_reference = Column(String(255), nullable=True)
    bible_text = Column(Text, nullable=True)
    difficulty = Column(SqlEnum(Difficulty), nullable=False)
    topic = Column(SqlEnum(Topics), nullable=False)
    tags = Column(JSON, nullable=True)
    hint = Column(Text, nullable=True)
    bible_reference_book = Column(SqlEnum(BibleBook), nullable=True)
    bible_reference_start_chapter = Column(Integer, nullable=True)
    bible_reference_end_chapter = Column(Integer, nullable=True)
    bible_reference_start_verse = Column(Integer, nullable=True)
    bible_reference_end_verse = Column(Integer, nullable=True)
    # Relationships
    section = relationship("Section", back_populates="questions")


class Score(Base):
    __tablename__ = 'scores'

    score_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    section_id = Column(Integer, ForeignKey('sections.section_id'), nullable=False)
    attempt_number = Column(Integer, nullable=False)
    score = Column(Integer, nullable=False)
    time_taken = Column(Integer, nullable=False)  # Time in seconds
    # Relationships
    user = relationship("User", back_populates="scores")
    section = relationship("Section", back_populates="scores")


class Progress(Base):
    __tablename__ = 'progresses'

    progress_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    section_id = Column(Integer, ForeignKey('sections.section_id'), nullable=False)
    question_id = Column(Integer, ForeignKey('questions.question_id'), nullable=False)
    is_correct = Column(Boolean, default=False)
    is_unsure = Column(Boolean, default=False)
    # Relationships
    user = relationship("User", back_populates="progresses")
    # Assuming Question model exists
    question = relationship("Question")


class BibleVerse(Base):
    __tablename__ = 'bible_verses'

    verse_id = Column(Integer, primary_key=True, index=True)
    book_name = Column(String(100), nullable=False)
    chapter = Column(Integer, nullable=False)
    verse = Column(Integer, nullable=False)
    text = Column(Text, nullable=False)
    version = Column(String(50), nullable=False)


class SectionCompletion(Base):
    __tablename__ = 'section_completions'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    section_id = Column(Integer, ForeignKey('sections.section_id'), nullable=False)
    time_taken_seconds = Column(Integer, nullable=False)
    bonus_points = Column(Integer, default=0)
    total_correct = Column(Integer, default=0)
    total_incorrect = Column(Integer, default=0)
    total_unsure = Column(Integer, default=0)
    date_completed = Column(DateTime, default=datetime.utcnow)
    # Relationships
    section = relationship("Section", back_populates="completions")
    user = relationship("User")

class Achievement(Base):
    __tablename__ = 'achievements'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    achievement_type = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    date_awarded = Column(DateTime, default=datetime.utcnow)
    # Relationships
    user = relationship("User", back_populates="achievements")
