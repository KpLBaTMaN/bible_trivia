import asyncio
import aiohttp
import json
import logging
import sys
import os

# Configure logging
logger = logging.getLogger('BulkUploadLogger')
logger.setLevel(logging.INFO)

# Create handlers
file_handler = logging.FileHandler('bulk_upload.log', mode='w')
file_handler.setLevel(logging.INFO)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)

# Create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

logger.info("Starting Bulk Upload Process")

# Load environment variables
NETWORK_IPV4_ADDRESS_BACKEND = os.getenv('NETWORK_IPV4_ADDRESS_BACKEND')

if not NETWORK_IPV4_ADDRESS_BACKEND:
    logger.error("Environment variable 'NETWORK_IPV4_ADDRESS_BACKEND' is not set.")
    sys.exit(1)

# Your API base URL
API_BASE_URL = f"http://{NETWORK_IPV4_ADDRESS_BACKEND}:8000"  # Change this to your actual API URL
logger.info(f"API Base URL set to: {API_BASE_URL}")

# Admin credentials
admin_credentials = {
    "username": os.getenv('ADMIN_USERNAME'),
    "password": os.getenv('ADMIN_PASSWORD'),
    "email": os.getenv('ADMIN_EMAIL')
}

missing_credentials = [key for key, value in admin_credentials.items() if not value]
if missing_credentials:
    logger.error(f"Missing admin credentials for: {', '.join(missing_credentials)}")
    sys.exit(1)

async def register_admin(session):
    logger.debug("Attempting to register admin user.")
    try:
        async with session.post(
            f"{API_BASE_URL}/users/register",
            json=admin_credentials
        ) as response:
            if response.status == 201:
                logger.info("Admin user registered successfully.")
            elif response.status == 400:
                logger.info("Admin user already exists.")
            else:
                text = await response.text()
                logger.error(f"Failed to register admin user. Status: {response.status}, Response: {text}")
    except Exception as e:
        logger.exception(f"Exception during admin registration: {e}")

async def login_admin(session):
    logger.debug("Attempting to log in admin user.")
    try:
        async with session.post(
            f"{API_BASE_URL}/users/login",
            data={
                "username": admin_credentials["username"],
                "password": admin_credentials["password"]
            }
        ) as response:
            if response.status == 200:
                data = await response.json()
                token = data.get("access_token")
                if token:
                    logger.info("Admin user logged in successfully.")
                    return token
                else:
                    logger.error("Login response missing 'access_token'.")
                    return None
            else:
                text = await response.text()
                logger.error(f"Failed to login admin user. Status: {response.status}, Response: {text}")
                return None
    except Exception as e:
        logger.exception(f"Exception during admin login: {e}")
        return None

async def get_sections(session, headers):
    logger.debug("Fetching existing sections.")
    try:
        async with session.get(
            f"{API_BASE_URL}/sections/",
            headers=headers
        ) as response:
            if response.status == 200:
                sections = await response.json()
                section_ids = {section['name']: section['section_id'] for section in sections}
                logger.info("Retrieved existing section IDs.")
                return section_ids
            else:
                text = await response.text()
                logger.error(f"Failed to retrieve sections. Status: {response.status}, Response: {text}")
                return {}
    except Exception as e:
        logger.exception(f"Exception during fetching sections: {e}")
        return {}

async def create_sections(session, headers, sections):
    logger.debug("Creating sections.")
    section_ids = {}
    for section in sections:
        try:
            async with session.post(
                f"{API_BASE_URL}/sections/",
                json=section,
                headers=headers
            ) as response:
                if response.status == 201:
                    section_data = await response.json()
                    section_ids[section['name']] = section_data['section_id']
                    logger.info(f"Section '{section['name']}' created with ID {section_data['section_id']}.")
                elif response.status == 400:
                    logger.info(f"Section '{section['name']}' may already exist. Attempting to retrieve its ID.")
                else:
                    text = await response.text()
                    logger.error(f"Failed to create section '{section['name']}'. Status: {response.status}, Response: {text}")
        except Exception as e:
            logger.exception(f"Exception during creating section '{section['name']}': {e}")
    
    # After attempting to create sections, get all sections to retrieve IDs
    existing_section_ids = await get_sections(session, headers)
    
    # Update section_ids with existing ones if not created in this run
    for section_name in [s['name'] for s in sections]:
        if section_name not in section_ids and section_name in existing_section_ids:
            section_ids[section_name] = existing_section_ids[section_name]
            logger.info(f"Section '{section_name}' retrieved with ID {existing_section_ids[section_name]}.")
        elif section_name not in existing_section_ids:
            logger.warning(f"Section '{section_name}' not found after creation attempt.")
    
    return section_ids

async def create_question(session, headers, question):
    logger.debug(f"Creating question: {question['question_text']}")
    try:
        async with session.post(
            f"{API_BASE_URL}/questions/",
            json=question,
            headers=headers
        ) as response:
            if response.status == 201 or response.status == 200:
                logger.info(f"Question '{question['question_text']}' created successfully.")
            else:
                text = await response.text()
                logger.error(f"Failed to create question '{question['question_text']}'. Status: {response.status}, Response: {text}")
    except Exception as e:
        logger.exception(f"Exception during creating question '{question['question_text']}': {e}")

async def create_questions_from_json(questions_data, session, headers, section_ids):
    logger.info(f"Starting to create questions from JSON file: {questions_data}")
    sem = asyncio.Semaphore(10)  # Limit concurrency to 10

    async def bound_create_question(question):
        async with sem:
            await create_question(session, headers, question)

    tasks = []

    logger.info(f"Loaded {len(questions_data)} questions from JSON file.")
    for item in questions_data:
        # Data validation
        if not all([item.get('section_name'), item.get('question_text'),
                    item.get('option1'), item.get('option2'), item.get('option3'),
                    item.get('option4'), item.get('correct_option')]):
            logger.warning(f"Skipping incomplete question: {item}")
            continue
        section_id = section_ids.get(item['section_name'])
        if not section_id:
            logger.warning(f"Section '{item['section_name']}' not found for question '{item['question_text']}'.")
            continue
        try:
            correct_option = int(item['correct_option'])
            if correct_option not in [1, 2, 3, 4]:
                logger.warning(f"Invalid 'correct_option' for question '{item['question_text']}': {item['correct_option']}. Must be 1-4.")
                continue
        except ValueError:
            logger.warning(f"Non-integer 'correct_option' for question '{item['question_text']}': {item['correct_option']}.")
            continue
        question = {
            "section_id": section_id,
            "question_text": item['question_text'],
            "option1": item['option1'],
            "option2": item['option2'],
            "option3": item['option3'],
            "option4": item['option4'],
            "correct_option": correct_option,
            "bible_reference": item.get('bible_reference', ''),
            "difficulty": item.get('difficulty', 'medium'),
            "topic": item.get('topic', 'general'),
            "hint": item.get('hint', '')
        }
        tasks.append(bound_create_question(question))
    

    if tasks:
        logger.info(f"Creating {len(tasks)} questions concurrently.")
        await asyncio.gather(*tasks)
        logger.info("Completed creating questions.")
    else:
        logger.warning("No valid questions to create.")

async def main():
    async with aiohttp.ClientSession() as session:
        # Register and login admin
        logger.info("Registering admin user.")
        await register_admin(session)
        logger.info("Logging in admin user.")
        token = await login_admin(session)
        if not token:
            logger.error("Cannot proceed without admin token. Exiting.")
            sys.exit(1)
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
     

        file_path = './data/combined_questions_with_sections.json'
        
        with open(file_path, mode='r', encoding='utf-8') as jsonfile:
            data = json.load(jsonfile)
        
        
        # Define sections
        sections = data["sections"]
        
        logger.info(f"Defining {len(sections)} sections.")
        # Create sections
        section_ids = await create_sections(session, headers, sections)
        if not section_ids:
            logger.error("No sections available after creation. Exiting.")
            sys.exit(1)
        logger.info(f"Section IDs obtained: {section_ids}")
        
        questions_data = data["questions"]
        
        # Create questions from JSON
        await create_questions_from_json(questions_data, session, headers, section_ids)

if __name__ == '__main__':
    try:
        asyncio.run(main())
        logger.info("Bulk upload process completed successfully.")
    except Exception as e:
        logger.exception(f"Unhandled exception in main: {e}")
        sys.exit(1)
