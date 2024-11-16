from fastapi import APIRouter

router = APIRouter()


@router.get(f"/health_check")
def health_check():
    return "active"
