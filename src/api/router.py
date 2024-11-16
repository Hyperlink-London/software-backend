from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from src.api.v1 import v1_router

router = APIRouter()
# router.include_router(v1_router, dependencies=[Depends(HTTPBearer(auto_error=False))])
router.include_router(v1_router)
