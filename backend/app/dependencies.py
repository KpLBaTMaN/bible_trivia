from fastapi import Depends
from .database import Database

def get_db():
    with Database() as db:
        yield db
