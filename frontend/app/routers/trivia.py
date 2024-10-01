# trivia.py
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests

from ..utils import get_current_user, API_BASE_URL

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

def process_questions(questions):
    for question in questions:
        # Combine the options into a list
        question['options'] = [
            question['option1'],
            question['option2'],
            question['option3'],
            question['option4'],
        ]
    return questions

def get_questions(section_id, headers):
    """Fetch questions for a given section from the API."""
    response = requests.get(f"{API_BASE_URL}/questions/section/{section_id}", headers=headers)
    if response.status_code == 200:
        questions = response.json()
        return process_questions(questions)
    else:
        return []

def submit_answers(section_id, answers, headers):
    """Submit user's answers to the API and receive feedback."""
    payload = {
        "section_id": section_id,
        "answers": answers
    }
    response = requests.post(
        f"{API_BASE_URL}/progress/submit",
        json=payload,
        headers=headers
    )
    if response.status_code == 200:
        return response.json()
    else:
        return []


def save_score(section_id, score, headers, attempt_number=0, time_taken=0):
    """Save the user's score to the backend."""
    payload = {
        "section_id": section_id,
        "attempt_number": attempt_number + 1,
        "score": score,
        "time_taken": time_taken
    }
    response = requests.post(
        f"{API_BASE_URL}/scores/",
        json=payload,
        headers=headers
    )
    return response.status_code == 200

def process_feedback(feedback, questions):
    """Enhance feedback with option texts based on user's answers."""
    questions_dict = {q['question_id']: q for q in questions}
    for item in feedback:
        question_id = item['question_id']
        question = questions_dict.get(question_id)
        if question:
            options = question['options']
            user_answer_index = item['user_answer'] - 1  # Convert to 0-based index
            correct_answer_index = item['correct_answer'] - 1
            item['user_answer_text'] = options[user_answer_index] if 0 <= user_answer_index < len(options) else 'Invalid option'
            item['correct_answer_text'] = options[correct_answer_index] if 0 <= correct_answer_index < len(options) else 'Invalid option'
        else:
            item['user_answer_text'] = 'Question not found'
            item['correct_answer_text'] = 'Question not found'
    return feedback

def get_attempt_number(section_id, user_id, headers):
    """Fetch the current attempt number for the section and user."""
    response = requests.get(
        f"{API_BASE_URL}/scores/attempts",
        params={"section_id": section_id, "user_id": user_id},
        headers=headers
    )
    if response.status_code == 200:
        # Assume the response contains an 'attempt_number' field
        return response.json()
    return 1  # Default to the first attempt if the API does not return data


def get_section_name(section_id, headers):
        # Fetch section
    sections_response = requests.get(f"{API_BASE_URL}/sections/{section_id}", headers=headers)
    if sections_response.status_code == 200:
        section = sections_response.json()
    else:
        section = {}
        
    section_name = section.get("name", section_id)
    
    return section_name


@router.get("/trivia/{section_id}", response_class=HTMLResponse)
def trivia_section(request: Request, section_id: int, user: dict = Depends(get_current_user)):
    headers = {"Authorization": f"Bearer {request.cookies.get('access_token')}"}
    questions = get_questions(section_id, headers)
    
    # Get Section Name
    section_name = get_section_name(section_id, headers)
    
    return templates.TemplateResponse("trivia.html", {
        "request": request,
        "user": user,
        "section": {"id": section_id, "name": f"Section: {section_name}"},
        "questions": questions,
        "user_answers": {},
        "total_questions": len(questions),
    })
    
    

    
    
@router.post("/trivia/{section_id}", response_class=HTMLResponse)
async def submit_trivia(request: Request, section_id: int, user: dict = Depends(get_current_user)):
    form = await request.form()
    user_answers  = {
        int(key[1:]): int(value)
        for key, value in form.items()
        if key.startswith("q") and key[1:].isdigit() and value.isdigit()
    }
    
    headers = {"Authorization": f"Bearer {request.cookies.get('access_token')}"}
    
    # Submit answers and get feedback
    feedback = submit_answers(section_id, user_answers, headers)
    
    # Get Section Name
    section_name = get_section_name(section_id, headers)
    
    
    # Calculate the user's score based on the feedback
    total_correct = sum(1 for item in feedback if item['result'] == "Correct")

    user_id = user.get("user_id")
    
    attempt_number = get_attempt_number(section_id=section_id, user_id=user_id, headers=headers)
    
    # Save the score
    save_score(section_id, total_correct, headers, attempt_number=attempt_number)
    
    # Fetch and process questions again for display
    questions = get_questions(section_id, headers)
    
    # Process feedback to include option text
    feedback = process_feedback(feedback, questions)

    return templates.TemplateResponse("trivia.html", {
        "request": request,
        "user": user,
        "section": {"id": section_id, "name": f"Section: {section_name}"},
        "questions": questions,
        "feedback": feedback,
        "user_answers": user_answers,
        "total_correct": total_correct,
        "total_questions": len(questions),
    })
    
   