import uvicorn
from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from src.api import router

api_prefix = ""

app = FastAPI(
    openapi_url=f"/hyperlink/api/openapi.json",
    docs_url=f"/hyperlink/api/docs",
    redoc_url=f"/hyperlink/api/redoc",
)


# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# app.include_router(router, prefix=api_prefix)
app.include_router(router, prefix=api_prefix)


if __name__ == "__main__":
    uvicorn.run("api_main:app", reload=True, host="0.0.0.0", port=8000)
