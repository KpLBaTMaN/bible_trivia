# routers/bible.py
import logging
from typing import List
import json

from fastapi import APIRouter, Depends, HTTPException, status
from .. import schemas, auth, database, dependencies

# Set up logging
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/bible",
    tags=["bible"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/", 
    response_model=List[schemas.BibleVerse]
)
def read_verses(
    skip: int = 0,
    limit: int = 100,
    db: database.Database = Depends(dependencies.get_db),
    current_user: schemas.User = Depends(auth.get_current_user)
):
    """
    Retrieve a list of Bible verses.
    """
    logger.info(f"User '{current_user.username}' is fetching Bible verses with skip={skip}, limit={limit}")
    try:
        verses = db.get_bible_verses(skip=skip, limit=limit)
        logger.info(f"Retrieved {len(verses)} Bible verses")
        return verses
    except Exception as e:
        logger.error(f"Error fetching Bible verses: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while fetching Bible verses.")

@router.get(
    "/{verse_id}", 
    response_model=schemas.BibleVerse
)
def read_verse(
    verse_id: int,
    db: database.Database = Depends(dependencies.get_db),
    current_user: schemas.User = Depends(auth.get_current_user)
):
    """
    Retrieve a specific Bible verse by ID.
    """
    logger.info(f"User '{current_user.username}' is fetching Bible verse with ID: {verse_id}")
    try:
        verse = db.get_bible_verse_by_id(verse_id=verse_id)
        if not verse:
            logger.warning(f"Bible verse with ID {verse_id} not found")
            raise HTTPException(status_code=404, detail="Bible verse not found.")
        return verse
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error fetching Bible verse with ID {verse_id}: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while fetching the Bible verse.")



# ----------- Admin Endpoints -------------



@router.post(
    "/", 
    response_model=schemas.BibleVerse, 
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(dependencies.require_role("admin"))]
)
def create_verse(
    verse: schemas.BibleVerseCreate,
    db: database.Database = Depends(dependencies.get_db),
    current_user: schemas.User = Depends(auth.get_current_user)
):
    """
    Create a new Bible verse.
    """
    logger.info(f"User '{current_user.username}' is creating a new Bible verse: {verse.book_name} {verse.chapter}:{verse.verse} ({verse.version})")
    try:
        # Check if the verse already exists
        existing_verse = db.get_bible_verse_by_details(
            book_name=verse.book_name, 
            chapter=verse.chapter, 
            verse=verse.verse, 
            version=verse.version
        )
        if existing_verse:
            logger.warning(f"Verse already exists: {verse.book_name} {verse.chapter}:{verse.verse} ({verse.version})")
            raise HTTPException(status_code=400, detail="Bible verse already exists.")
        
        new_verse = db.create_bible_verse(verse=verse)
        logger.info(f"Successfully created Bible verse with ID: {new_verse.verse_id}")
        return new_verse
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error creating Bible verse: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while creating the Bible verse.")






@router.put(
    "/{verse_id}", 
    response_model=schemas.BibleVerse,
    dependencies=[Depends(dependencies.require_role("admin"))]
)
def update_verse(
    verse_id: int,
    verse_update: schemas.BibleVerseCreate,
    db: database.Database = Depends(dependencies.get_db),
    current_user: schemas.User = Depends(auth.get_current_user)
):
    """
    Update an existing Bible verse.
    """
    logger.info(f"User '{current_user.username}' is updating Bible verse with ID: {verse_id}")
    try:
        updated_verse = db.update_bible_verse(verse_id=verse_id, verse_update=verse_update)
        if not updated_verse:
            logger.warning(f"Bible verse with ID {verse_id} not found for update")
            raise HTTPException(status_code=404, detail="Bible verse not found.")
        logger.info(f"Successfully updated Bible verse with ID: {verse_id}")
        return updated_verse
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error updating Bible verse with ID {verse_id}: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while updating the Bible verse.")




@router.delete(
    "/{verse_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(dependencies.require_role("admin"))]
)
def delete_verse(
    verse_id: int,
    db: database.Database = Depends(dependencies.get_db),
    current_user: schemas.User = Depends(auth.get_current_user)
):
    """
    Delete a Bible verse by ID.
    """
    logger.info(f"User '{current_user.username}' is deleting Bible verse with ID: {verse_id}")
    try:
        success = db.delete_bible_verse(verse_id=verse_id)
        if not success:
            logger.warning(f"Bible verse with ID {verse_id} not found for deletion")
            raise HTTPException(status_code=404, detail="Bible verse not found.")
        logger.info(f"Successfully deleted Bible verse with ID: {verse_id}")
        return
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error deleting Bible verse with ID {verse_id}: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while deleting the Bible verse.")
    
    

@router.post(
    "/batch", 
    response_model=List[schemas.BibleVerse], 
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(dependencies.require_role("admin"))]
)
def create_verses_in_batch(
    verses: List[schemas.BibleVerseCreate],
    db: database.Database = Depends(dependencies.get_db),
    current_user: schemas.User = Depends(auth.get_current_user)
):
    """
    Create multiple Bible verses in batch.
    """
    created_verses = []
    logger.info(f"User '{current_user.username}' is creating {len(verses)} Bible verses in batch.")
    try:
        for verse in verses:
            # Check if the verse already exists
            existing_verse = db.get_bible_verse_by_details(
                book_name=verse.book_name, 
                chapter=verse.chapter, 
                verse=verse.verse, 
                version=verse.version
            )
            if existing_verse:
                continue  # Skip this verse if it already exists

            new_verse = db.create_bible_verse(verse=verse)
            created_verses.append(new_verse)
            
        logger.info(f"Successfully created {len(created_verses)} Bible verses.")
        return created_verses
    except Exception as e:
        logger.error(f"Error creating Bible verses in batch: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while creating the Bible verses.")

# Load JSON from file and create verses
def load_verses_from_json(file_path: str, db: database.Database):
    """
    Load Bible verses from a JSON file and insert them into the database.
    """
    created_verses = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                verse_data = json.loads(line.strip())  # Parse each line as JSON
                verse = schemas.BibleVerseCreate(
                    book_name=verse_data["book_name"],
                    book_id=verse_data["book_id"],
                    chapter=verse_data["chapter"],
                    verse=verse_data["verse"],
                    text=verse_data["text"],
                    version=verse_data["translation_id"]
                )
                # Create each verse using the db.create_bible_verse method
                existing_verse = db.get_bible_verse_by_details(
                    book_name=verse.book_name, 
                    chapter=verse.chapter, 
                    verse=verse.verse, 
                    version=verse.version
                )
                if not existing_verse:
                    new_verse = db.create_bible_verse(verse=verse)
                    created_verses.append(new_verse)
                else:
                    logger.info(f"Verse already exists: {verse.book_name} {verse.chapter}:{verse.verse} ({verse.version})")

        logger.info(f"Successfully created {len(created_verses)} verses from JSON.")
        return created_verses

    except Exception as e:
        logger.error(f"Error loading verses from JSON file {file_path}: {e}")
        raise e