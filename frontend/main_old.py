from fastapi import FastAPI, Request, Depends, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import Optional
import os  # For environment variable


from backend import auth, crud, schemas, database

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="frontend/templates")

# Dependency to get DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Middleware for session management (simple example using cookies)
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helper to get current user from cookie
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

SECRET_KEY = "your-secret-key"  # Use environment variable in production
ALGORITHM = "HS256"

def get_current_user_token(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return username

def get_current_user_template(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        user = crud.get_user_by_username(db, username=username)
        return user
    except JWTError:
        return None

# Home Page
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request, current_user: Optional[schemas.User] = Depends(get_current_user_template)):
    return templates.TemplateResponse("index.html", {"request": request, "user": current_user})

# Register Page
@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request, "user": None})

@app.post("/register", response_class=HTMLResponse)
def register(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username=username)
    if user:
        return templates.TemplateResponse("register.html", {"request": request, "error": "Username already exists"})
    new_user = crud.create_user(db, schemas.UserCreate(username=username, password=password))
    return RedirectResponse(url="/login", status_code=303)

# Login Page
@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "user": None})

@app.post("/login", response_class=HTMLResponse)
def login(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username=username)
    if not user or not auth.verify_password(password, user.password_hash):
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})
    access_token = auth.create_access_token(data={"sub": user.username})
    response = RedirectResponse(url="/sections", status_code=303)
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return response

# Logout
@app.get("/logout")
def logout():
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie("access_token")
    return response

# Sections Page
@app.get("/sections", response_class=HTMLResponse)
def sections_page(request: Request, db: Session = Depends(get_db), current_user: Optional[schemas.User] = Depends(get_current_user_template)):
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)
    sections = crud.get_sections(db)
    return templates.TemplateResponse("sections.html", {"request": request, "sections": sections, "user": current_user})

# Quiz Page
@app.get("/quiz/{section_id}", response_class=HTMLResponse)
def quiz_page(request: Request, section_id: int, db: Session = Depends(get_db), current_user: Optional[schemas.User] = Depends(get_current_user_template)):
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)
    section = crud.get_section(db, section_id=section_id)
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    return templates.TemplateResponse("quiz.html", {"request": request, "section": section, "user": current_user})

# Scoreboard Page
@app.get("/scoreboard", response_class=HTMLResponse)
def scoreboard_page(request: Request, db: Session = Depends(get_db), current_user: Optional[schemas.User] = Depends(get_current_user_template)):
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)
    scores = crud.get_all_scores(db)
    return templates.TemplateResponse("scoreboard.html", {"request": request, "scores": scores, "user": current_user})
