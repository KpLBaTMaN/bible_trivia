# app/routers/about_contact.py
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import status
from starlette.responses import RedirectResponse

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# About Page
@router.get("/about", response_class=HTMLResponse)
def about_view(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

# Contact Page (GET and POST)
@router.get("/contact", response_class=HTMLResponse)
def contact_view(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})

@router.post("/contact", response_class=HTMLResponse)
def submit_contact(request: Request, name: str = Form(...), email: str = Form(...), message: str = Form(...)):
    # Here, you can add logic to send the form data via email or store it in a database
    print(f"Name: {name}, Email: {email}, Message: {message}")
    
    # Redirect back to the contact page with a thank you message
    return templates.TemplateResponse("contact.html", {
        "request": request,
        "message": "Thank you for getting in touch!"
    })
