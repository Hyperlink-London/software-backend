from fastapi import APIRouter

from src.api.v1.checkers import router as health_check_router
from src.api.v1.pod_data import router as command_router
from src.api.v1.test import router as test_router
router = APIRouter(prefix="/v1")


router.include_router(health_check_router)
router.include_router(command_router)
router.include_router(test_router)
