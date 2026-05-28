import os

from fastapi import APIRouter, HTTPException
from sqlalchemy import text
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv

from db.database import engine
from schemas.auth import UserSignup, UserLogin

load_dotenv()

router = APIRouter()

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

SECRET_KEY = os.getenv("SECRET_KEY")

ALGORITHM = "HS256"


# -----------------------------
# SIGNUP
# -----------------------------
@router.post("/signup")
def signup(user: UserSignup):

    hashed_password = pwd_context.hash(user.password)

    with engine.connect() as connection:

        # Check if email already exists
        existing_user = connection.execute(
            text("""
                SELECT * FROM users
                WHERE email = :email
            """),
            {
                "email": user.email
            }
        ).fetchone()

        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )

        # Insert new user
        connection.execute(
            text("""
                INSERT INTO users (
                    username,
                    email,
                    password_hash
                )
                VALUES (
                    :username,
                    :email,
                    :password_hash
                )
            """),
            {
                "username": user.username,
                "email": user.email,
                "password_hash": hashed_password
            }
        )

        connection.commit()

    return {
        "message": "User created successfully"
    }


# -----------------------------
# LOGIN
# -----------------------------
@router.post("/login")
def login(user: UserLogin):

    with engine.connect() as connection:

        db_user = connection.execute(
            text("""
                SELECT *
                FROM users
                WHERE email = :email
            """),
            {
                "email": user.email
            }
        ).fetchone()

        if not db_user:
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials"
            )

        valid_password = pwd_context.verify(
            user.password,
            db_user.password_hash
        )

        if not valid_password:
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials"
            )

        # Create JWT token
        token_data = {
            "user_id": db_user.id,
            "email": db_user.email,
            "exp": datetime.utcnow() + timedelta(hours=24)
        }

        token = jwt.encode(
            token_data,
            SECRET_KEY,
            algorithm=ALGORITHM
        )

    return {
        "access_token": token,
        "token_type": "bearer"
    }