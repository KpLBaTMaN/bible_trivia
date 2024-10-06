# app/routers/auth.py

from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import requests

from ..utils import API_BASE_URL

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/register", response_class=HTMLResponse)
def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.post("/register", response_class=HTMLResponse)
def register(
    request: Request, 
    username: str = Form(...), 
    password: str = Form(...)
):
    data = {"username": username, "password": password}
    try:
        response = requests.post(f"{API_BASE_URL}/users/register", json=data)
    except requests.exceptions.RequestException as e:
        return templates.TemplateResponse("register.html", {"request": request, "error": str(e)})
    
    print("Response: ", response.status_code)
    
    if response.status_code == 201 or response.status_code == 200:
        return RedirectResponse(url="/login", status_code=303)
    elif response.status_code == 400:
        error = response.json().get("detail", "Invalid input data")
    else:
        error = "Registration failed. Please try again."
    return templates.TemplateResponse("register.html", {"request": request, "error": error})

@router.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login", response_class=HTMLResponse)
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    data = {"username": username, "password": password}
    response = requests.post(f"{API_BASE_URL}/users/login", data=data)
    if response.status_code == 200:
        token = response.json().get("access_token")
        response = RedirectResponse(url="/dashboard", status_code=303)
        response.set_cookie(key="access_token", value=token, httponly=True, secure=False, samesite='Lax')
        return response
    else:
        error = response.json().get("detail", "Login failed")
        return templates.TemplateResponse("login.html", {"request": request, "error": error})
