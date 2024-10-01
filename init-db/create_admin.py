import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext


from create_account.models import User, Base
from create_account.enums import Role

# Load environment variables
DATABASE_URL = os.getenv('DATABASE_URL')

# Admin Website
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME')
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')

print(f"DATABASE_URL: {DATABASE_URL}")
print(f"ADMIN_USERNAME: {ADMIN_USERNAME}")
print(f"ADMIN_PASSWORD: {ADMIN_PASSWORD}")
print(f"ADMIN_EMAIL: {ADMIN_EMAIL}")

# Establish database connection
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Password context for hashing and verifying
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def get_password_hash(password: str) -> str:
    """Hash a password for storing in the database."""
    return pwd_context.hash(password)

def create_admin_user():
    """Create an admin user for testing purposes."""
    session = SessionLocal()

    # Hash the password using the provided get_password_hash function
    password_hash = get_password_hash(ADMIN_PASSWORD)

    try:
        # Check if the admin user already exists
        existing_user = session.query(User).filter(User.username == ADMIN_USERNAME).first()
        
        if existing_user:
            print(f"Admin user '{ADMIN_USERNAME}' already exists.")
        else:
            # Create a new admin user
            admin_user = User(
                username=ADMIN_USERNAME,
                email=ADMIN_EMAIL,
                password_hash=password_hash,
                role=Role.admin
            )
            session.add(admin_user)
            session.commit()
            print(f"Admin user '{ADMIN_USERNAME}' created successfully.")
    except IntegrityError as e:
        # Handle any potential errors such as duplicate email or username
        session.rollback()
        print(f"Error creating admin user: {e}")
    finally:
        session.close()


# Create the admin user
create_admin_user()

print("Finished Create Admin Python")
