import os
import json
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Load environment variables
DATABASE_URL = os.getenv('DATABASE_URL')

# Establish database connection
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

### MODELS ###
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
    difficulty = Column(String(50), nullable=False)
    tags = Column(Text, nullable=True)  # Store as comma-separated string or JSON
    topic = Column(String(255), nullable=True)
    hint = Column(String(500), nullable=True)
    bible_reference_book = Column(String(100), nullable=True)
    bible_reference_start_chapter = Column(Integer, nullable=True)
    bible_reference_end_chapter = Column(Integer, nullable=True)
    bible_reference_start_verse = Column(Integer, nullable=True)
    bible_reference_end_verse = Column(Integer, nullable=True)

    section = relationship('Section', back_populates='questions')

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

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

### DATA POPULATION FUNCTIONS ###
def load_bible_verses():
    """Populate the BibleVerse table from a JSON file."""
    session = SessionLocal()
    try:
        # Path to your JSON file (change the path as needed)
        BIBLE_VERSES_JSON_FILE_PATH = os.path.join(os.path.dirname(__file__), 'data/kjv.json')
        
        with open(BIBLE_VERSES_JSON_FILE_PATH, 'r', encoding='utf-8') as file:
            for line in file:
                verse_data = json.loads(line)
                # Create a BibleVerse object from the JSON data
                new_verse = BibleVerse(
                    book_name=verse_data['book_name'],
                    chapter=verse_data['chapter'],
                    verse=verse_data['verse'],
                    text=verse_data['text'],
                    version=verse_data.get('translation_id', 'KJV')
                )
                session.add(new_verse)
        session.commit()
        print("Bible verses successfully added to the database.")
    except Exception as e:
        session.rollback()
        print(f"An error occurred while loading Bible verses: {e}")
    finally:
        session.close()

def load_questions_and_sections():
    """Populate the Section and Question tables from a JSON file."""
    session = SessionLocal()
    try:
        # Path to your JSON file (change the path as needed)
        QUESTIONS_JSON_FILE_PATH = os.path.join(os.path.dirname(__file__), 'data/questions.json')
        
        with open(QUESTIONS_JSON_FILE_PATH, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for section_key, section_data in data.items():
                # Parse section information from key (e.g., "Genesis_37_50")
                book_name, start_chapter, end_chapter = section_key.split('_')
                
                # Create a new Section object
                new_section = Section(
                    name=section_data.get('topic', 'Unnamed Section'),
                    description=section_data.get('description', f"Questions from {book_name} {start_chapter}-{end_chapter}")
                )
                session.add(new_section)
                session.flush()  # Flush to get the section_id

                for question_data in section_data['questions']:
                    # Parse and create Question object
                    options = question_data['options']
                    new_question = Question(
                        section_id=new_section.section_id,
                        question_text=question_data['question_text'],
                        option1=options[0],
                        option2=options[1],
                        option3=options[2],
                        option4=options[3],
                        correct_option=question_data['correct_option_index'],
                        bible_reference=question_data['bible_reference'],
                        difficulty=question_data['difficulty'],
                        tags=",".join(question_data['tags']),  # Store as comma-separated string
                        topic=question_data['topic'],
                        hint=question_data.get('hint'),
                        bible_reference_book=question_data['bible_reference_book'],
                        bible_reference_start_chapter=question_data['bible_reference_start_chapter'],
                        bible_reference_end_chapter=question_data['bible_reference_end_chapter'],
                        bible_reference_start_verse=question_data['bible_reference_start_verse'],
                        bible_reference_end_verse=question_data['bible_reference_end_verse']
                    )
                    session.add(new_question)
        
        session.commit()
        print("Questions and sections successfully added to the database.")
    except Exception as e:
        session.rollback()
        print(f"An error occurred while loading questions and sections: {e}")
    finally:
        session.close()

def create_default_user():
    """Create a default user for testing purposes."""
    session = SessionLocal()
    try:
        default_user = User(
            username="testuser",
            password_hash="hashedpassword",  # Normally, you'd hash the password securely
            email="testuser@example.com",
            total_score=0
        )
        session.add(default_user)
        session.commit()
        print("Default user added to the database.")
    except Exception as e:
        session.rollback()
        print(f"An error occurred while creating the default user: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    # Populate Bible verses
    load_bible_verses()

    # Populate sections and questions
    load_questions_and_sections()

    # Create a default user (optional)
    create_default_user()
