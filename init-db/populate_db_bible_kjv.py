import json
import os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Load environment variables
DATABASE_URL = os.getenv('DATABASE_URL')

# Establish database connection
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define the BibleVerse model
class BibleVerse(Base):
    __tablename__ = "bible_verses"
    
    id = Column(Integer, primary_key=True, index=True)
    book_name = Column(String(100), nullable=False)
    chapter = Column(Integer, nullable=False)
    verse = Column(Integer, nullable=False)
    text = Column(String(2000), nullable=False)  # Adjust the length as needed
    version = Column(String(50), default="KJV", nullable=False)

# Create the table if it doesn't exist
Base.metadata.create_all(bind=engine)

# Path to your JSON file (located in the "data" directory within "init-db")
JSON_FILE_PATH = os.path.join(os.path.dirname(__file__), 'data/kjv.json')

def load_bible_verses():
    # Create a new session
    session = SessionLocal()
    
    try:
        # Open the JSON file and read each line as a separate JSON object
        with open(JSON_FILE_PATH, 'r', encoding='utf-8') as file:
            for line in file:
                verse_data = json.loads(line)
                
                # Create a BibleVerse object
                new_verse = BibleVerse(
                    book_name=verse_data['book_name'],
                    chapter=verse_data['chapter'],
                    verse=verse_data['verse'],
                    text=verse_data['text'],
                    version=verse_data.get('translation_id', 'KJV')  # Default to "KJV"
                )
                
                # Add the object to the session
                session.add(new_verse)
        
        # Commit all changes to the database
        session.commit()
        print("Bible verses successfully added to the database.")
    
    except Exception as e:
        session.rollback()
        print(f"An error occurred: {e}")
    
    finally:
        session.close()

if __name__ == "__main__":
    load_bible_verses()
