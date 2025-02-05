from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
from fastapi import APIRouter
from random import randint
import pandas as pd

router = APIRouter()


@router.get(f"/health_check")
def health_check():
    return "active"


@router.get("/random_data")
def random_data():
    start_time = datetime.now()
    data = {
        "x": [(start_time + timedelta(seconds=i * 5)).isoformat() for i in range(10)],
        "y": [randint(0, 100) for _ in range(10)]
    }

    df = pd.DataFrame(data)
    return JSONResponse(content=df.to_dict(orient="records"))
