# app/routers/leaderboard.py
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests

from ..utils import get_current_user, API_BASE_URL

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/leaderboard", response_class=HTMLResponse)
def leaderboard_view(request: Request, user: dict = Depends(get_current_user)):
    headers = {"Authorization": f"Bearer {request.cookies.get('access_token')}"}
    
    # Fetch global leaderboard
    global_response = requests.get(f"{API_BASE_URL}/leaderboard/global", headers=headers)
    if global_response.status_code == 200:
        global_leaderboard = global_response.json()
    else:
        global_leaderboard = []

    # Fetch sections
    sections_response = requests.get(f"{API_BASE_URL}/sections", headers=headers)
    sections = sections_response.json() if sections_response.status_code == 200 else []
    
    # Fetch section leaderboards
    section_leaderboards = []
    for section in sections:
        sec_id = section['section_id']  # Changed from 'id' to 'section_id'
        sec_response = requests.get(f"{API_BASE_URL}/leaderboard/section/{sec_id}", headers=headers)
        if sec_response.status_code == 200:
            section_leaderboards.append({
                "section": section['name'],
                "leaderboard": sec_response.json()
            })
        else:
            # Handle cases where the section leaderboard is not available
            section_leaderboards.append({
                "section": section['name'],
                "leaderboard": []
            })
    
    return templates.TemplateResponse("leaderboard.html", {
        "request": request,
        "user": user,
        "global_leaderboard": global_leaderboard,
        "sections": section_leaderboards
    })
