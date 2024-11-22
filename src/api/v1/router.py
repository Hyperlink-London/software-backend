from fastapi import APIRouter

from src.api.v1.checkers import router as checker_router
from src.api.v1.pod_data import router as pod_data_router
# from src.api.v1.pod_states import router as pod_states_router
# from src.api.v1.pod_battery import router as pod_battery_router

router = APIRouter(prefix="/v1")

router.include_router(checker_router)
router.include_router(pod_data_router)
