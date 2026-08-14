from fastapi import APIRouter, Depends

from app.auth.dependencies import get_current_user


router = APIRouter(
    prefix="/protected",
    tags=["Protected"],
)


@router.get("/profile")
def profile(current_user=Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
    }
    
    
    