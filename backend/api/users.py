from fastapi import APIRouter, Depends

from utils.auth import get_current_user

router = APIRouter()


@router.get("/me")
def get_me(
    current_user=Depends(get_current_user)
):

    return {
        "user": current_user
    }