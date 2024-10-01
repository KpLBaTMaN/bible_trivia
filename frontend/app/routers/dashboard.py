# app/routers/dashboard.py
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests

from ..utils import get_current_user, API_BASE_URL

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/dashboard", response_class=HTMLResponse)
def dashboard_view(request: Request, user: dict = Depends(get_current_user)):
    headers = {"Authorization": f"Bearer {request.cookies.get('access_token')}"}

    # Fetch available sections
    sections_response = requests.get(f"{API_BASE_URL}/sections", headers=headers)
    if sections_response.status_code == 200:
        sections = sections_response.json()
    else:
        sections = []

    # Fetch user's scores for sections
    scores_response = requests.get(f"{API_BASE_URL}/scores/my-scores", headers=headers)
    if scores_response.status_code == 200:
        scores_data = scores_response.json()
        # Process scores_data to get the latest score per section
        scores_by_section = {}
        for score in scores_data:
            section_id = score['section_id']
            attempt_number = score['attempt_number']
            # Keep the score with the highest attempt_number (latest attempt)
            if section_id not in scores_by_section or attempt_number > scores_by_section[section_id]['attempt_number']:
                scores_by_section[section_id] = score
    else:
        scores_by_section = {}

    # Merge scores into sections
    completed_sections = 0
    for section in sections:
        section_id = section['section_id']
        score_entry = scores_by_section.get(section_id)
        if score_entry:
            section['score'] = score_entry['score']
            completed_sections += 1
        else:
            section['score'] = None

    total_sections = len(sections)
    remaining_sections = total_sections - completed_sections

    # Update progress to reflect sections completed
    progress = {
        "completed_sections": completed_sections,
        "remaining_sections": remaining_sections,
    }

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": user,
        "progress": progress,
        "sections": sections
    })
