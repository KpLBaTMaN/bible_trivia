# app/main.py
from fastapi import FastAPI, Request, Form, Depends, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests
from .routers import auth, dashboard, leaderboard, trivia
from .utils import get_current_user, API_BASE_URL
import uvicorn
import os


app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Set up templates
templates = Jinja2Templates(directory="app/templates")

# Include routers
app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(leaderboard.router)
app.include_router(trivia.router)

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    token = request.cookies.get("access_token")
    user = None
    if token:
        try:
            user_response = requests.get(
                f"{API_BASE_URL}/users/me",
                headers={"Authorization": f"Bearer {token}"}
            )
            if user_response.status_code == 200:
                user = user_response.json()
        except:
            pass
    return templates.TemplateResponse("home.html", {"request": request, "user": user})

# Logout route
@app.get("/logout")
def logout():
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie(key="access_token")
    return response