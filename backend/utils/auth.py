from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy import text
from dotenv import load_dotenv
from pathlib import Path
import os

from db.database import engine

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("user_id")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        with engine.connect() as connection:

            user = connection.execute(
                text("""
                    SELECT id, username, email
                    FROM users
                    WHERE id = :user_id
                """),
                {
                    "user_id": user_id
                }
            ).fetchone()

            if not user:
                raise HTTPException(
                    status_code=401,
                    detail="User not found"
                )

            return {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )