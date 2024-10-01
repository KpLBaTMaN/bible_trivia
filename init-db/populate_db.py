import requests
import json
import os

print("Running Populate DB")
# Load environment variables
NETWORK_IPV4_ADDRESS_BACKEND = os.getenv('NETWORK_IPV4_ADDRESS_BACKEND')

# Your API base URL
BASE_URL = f"http://{NETWORK_IPV4_ADDRESS_BACKEND}:8000"  # Change this to your actual API URL

# Admin Website
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')

print(f"ADMIN_USERNAME: {ADMIN_USERNAME}")
print(f"ADMIN_PASSWORD: {ADMIN_PASSWORD}")

# Path to the JSON file with the verses data
JSON_FILE_PATH = 'data/kjv.json'

# Function to login and get the access token
def login(username, password):
    login_url = f"{BASE_URL}/users/login"
    # Use the OAuth2PasswordRequestForm structure
    login_data = {
        "username": username,
        "password": password
    }
    
    response = requests.post(login_url, data=login_data)
    
    if response.status_code == 200:
        token = response.json().get("access_token")
        print(f"Login successful. Token received: {token}")
        return token
    else:
        print(f"Login failed: {response.status_code}, {response.text}")
        return None

# Function to add verses in batch
def add_verses_batch(verses, headers):
    print("Posting Batch")
    bible_batch_url = f"{BASE_URL}/bible/batch"
    response = requests.post(bible_batch_url, headers=headers, json=verses)
    
    if response.status_code == 201:
        print(f"Successfully added {len(verses)} verses in batch.")
    else:
        print(f"Failed to add verses in batch.")
        print(f"Status Code: {response.status_code}, Response: {response.text}")

# Load the data from the JSON file
def load_verses_data(file_path):
    print("Load Verses")
    with open(file_path, 'r') as file:
        return [json.loads(line) for line in file]

# Prepare the verses data to match the expected schema
def prepare_verses_data(raw_data):
    print("Prepare Verses Data")
    prepared_data = []
    for verse in raw_data:
        prepared_data.append({
            "book_name": verse["book_name"],
            "book_id": verse["book_id"],
            "chapter": verse["chapter"],
            "verse": verse["verse"],
            "text": verse["text"],
            "version": verse["translation_id"]
        })
    return prepared_data

# Main logic
def main():
    # Step 1: Login and get access token
    token = login(ADMIN_USERNAME, ADMIN_PASSWORD)
    
    if not token:
        print("Exiting script due to login failure.")
        return
    
    # Step 2: Set up headers for authorized requests
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Step 3: Load the verses data
    raw_verses_data = load_verses_data(JSON_FILE_PATH)
    
    # Step 4: Prepare the data to match the schema expected by the API
    verses_data = prepare_verses_data(raw_verses_data)
    
    # Step 5: Add verses using the batch endpoint
    add_verses_batch(verses_data, headers)


main()
print("End of populate_db.py")
