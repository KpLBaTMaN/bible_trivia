from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # Import CORS middleware
from .routers import users, sections, questions, scores
from .database import engine
from .models import Base
from .logging_config import setup_logging

setup_logging()

# Creating the Database Table
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, replace with ["http://localhost:3000"] for security
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

app.include_router(users.router)
app.include_router(sections.router)
app.include_router(questions.router)
app.include_router(scores.router)