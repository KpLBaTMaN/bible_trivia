# schemas.py
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
from .enums import Difficulty, Role, BibleBook, Topics, Tag
from typing import Dict

# ---------------- User Schemas ----------------

# Base class for shared attributes
class UserBase(BaseModel):
    username: str

# Schema for user creation input
class UserCreate(BaseModel):
    username: str
    password: str

# Schema for user output, includes role and other fields
class User(UserBase):
    user_id: int
    role: Role

    class Config:
        orm_mode = True

# ---------------- Section Schemas ----------------

class SectionBase(BaseModel):
    name: str
    description: Optional[str] = None

class SectionCreate(SectionBase):
    pass

class Section(SectionBase):
    section_id: int
    total_questions: int  # Add this field

    class Config:
        orm_mode = True

# ---------------- Question Schemas ----------------

class QuestionBase(BaseModel):
    section_id: int
    question_text: str
    option1: str
    option2: str
    option3: str
    option4: str
    correct_option: int
    bible_reference: str
    bible_text: Optional[str] = None
    difficulty: Difficulty  # e.g., "Beginner", "Intermediate", "Advanced"
    topic: Topics
    tags: Optional[List[Tag]] = []
    hint: Optional[str] = None
    bible_reference_book: Optional[BibleBook] = None
    bible_reference_start_chapter: Optional[int] = None
    bible_reference_end_chapter: Optional[int] = None
    bible_reference_start_verse: Optional[int] = None
    bible_reference_end_verse: Optional[int] = None

class QuestionCreate(QuestionBase):
    pass

class Question(QuestionBase):
    question_id: int

    class Config:
        orm_mode = True

# ---------------- Score Schemas ----------------

class ScoreBase(BaseModel):
    section_id: int
    attempt_number: int
    score: int
    time_taken: int  # Time in seconds


class ScoreCreate(ScoreBase):
    pass


class ScoreOut(ScoreBase):
    score_id: int
    user_id: int

    class Config:
        orm_mode = True

# ---------------- Bible Verse Schemas ----------------

class BibleVerseBase(BaseModel):
    book_name: str
    chapter: int
    verse: int
    text: str
    version: str

class BibleVerseCreate(BibleVerseBase):
    pass

class BibleVerse(BibleVerseBase):
    verse_id: int

    class Config:
        orm_mode = True

# ---------------- Progress Schemas ----------------

class ProgressBase(BaseModel):
    user_id: int
    section_id: int
    question_id: int
    is_correct: bool
    is_unsure: bool


class ProgressCreate(ProgressBase):
    pass

class Progress(ProgressBase):
    progress_id: int


    class Config:
        orm_mode = True

class SectionPerformance(BaseModel):
    total_correct: int
    total_incorrect: int
    total_unsure: int

    class Config:
        orm_mode = True
        
        
class ProgressSubmission(BaseModel):
    section_id: int
    answers: Dict[int, int]  # Mapping from question_id to user's answer

class ProgressFeedback(BaseModel):
    question_id: int
    question_text: str
    user_answer: int  # Changed from str to int
    correct_answer: int  # Changed from str to int
    result: str  # "Correct" or "Incorrect"
    explanation: Optional[str] = None


# ---------------- Leaderboard Schemas ----------------

class UserScore(BaseModel):
    username: str
    total_score: int

    class Config:
        orm_mode = True

# ---------------- Achievement Schemas ----------------

class AchievementBase(BaseModel):
    user_id: int
    achievement_type: str
    description: Optional[str] = None

class AchievementCreate(AchievementBase):
    date_awarded: Optional[datetime] = None

class Achievement(AchievementBase):
    id: int
    date_awarded: datetime

    class Config:
        orm_mode = True

# ---------------- Section Completion Schemas ----------------

class SectionCompletion(BaseModel):
    user_id: int
    section_id: int
    time_taken_seconds: int
    bonus_points: int
    total_correct: int
    total_incorrect: int
    total_unsure: int

class SectionCompletionResponse(BaseModel):
    total_correct: int
    total_incorrect: int
    total_unsure: int
    bible_verses: List[str]
    final_score: int

    class Config:
        orm_mode = True

class SectionCompletionDetail(BaseModel):
    total_correct: int
    total_incorrect: int
    total_unsure: int
    bible_verses: List[str]
    final_score: int

    class Config:
        orm_mode = True