# app/utils.py
from fastapi import Request, HTTPException, Depends
from fastapi.responses import RedirectResponse
import requests
import os


# Load environment variables
NETWORK_IPV4_ADDRESS_BACKEND = os.getenv('NETWORK_IPV4_ADDRESS_BACKEND')

# Your API base URL
API_BASE_URL = f"http://{NETWORK_IPV4_ADDRESS_BACKEND}:8000"  # Change this to your actual API URL
print("API_BASE_URL: ", API_BASE_URL)


def get_token_from_cookie(request: Request):
    return request.cookies.get("access_token")

def is_authenticated(token: str):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_BASE_URL}/users/me", headers=headers)
    return response.status_code == 200

def get_current_user(request: Request):
    token = get_token_from_cookie(request)
    if not token or not is_authenticated(token):
        raise HTTPException(status_code=401, detail="Not authenticated")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_BASE_URL}/users/me", headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid token")
    return response.json()
