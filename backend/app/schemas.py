from pydantic import BaseModel, EmailStr
from typing import List, Optional

from app.enums import Topics, Difficulty, BibleBook, Tag


### USER
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    user_id: int
    total_score: int

    class Config:
        orm_mode = True

### QUESTION

class QuestionBase(BaseModel):
    section_id: int
    question_text: str
    option1: str
    option2: str
    option3: str
    option4: str
    bible_reference: str
    difficulty: Difficulty  
    tags: List[Tag]  # Now using the Tag enum
    topic: Optional[Topics] = None  # Now using the Topics enum
    hint: Optional[str] = None
    bible_reference_book: BibleBook
    bible_reference_start_chapter: int
    bible_reference_end_chapter: int
    bible_reference_start_verse: int
    bible_reference_end_verse: int

class QuestionCreate(QuestionBase):
    correct_option: int
    bible_text: Optional[str] = None

class Question(QuestionBase):
    question_id: int

    class Config:
        orm_mode = True

### SECTION
class SectionBase(BaseModel):
    name: str
    description: Optional[str] = None

class SectionCreate(SectionBase):
    pass

class Section(SectionBase):
    section_id: int
    questions: List[Question] = []

    class Config:
        orm_mode = True

### SCORES
class ScoreBase(BaseModel):
    section_id: int
    attempt_number: int
    score: int
    time_taken: int

class ScoreCreate(ScoreBase):
    pass

class Score(ScoreBase):
    score_id: int
    user_id: int

    class Config:
        orm_mode = True

## BIBLE
class BibleVerseBase(BaseModel):
    book_name: str
    chapter: int
    verse: int
    text: str
    version: Optional[str] = "KJV"  # Default to KJV

class BibleVerseCreate(BibleVerseBase):
    pass

class BibleVerse(BibleVerseBase):
    id: int

    class Config:
        orm_mode = True
