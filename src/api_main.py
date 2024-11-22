import uvicorn
from fastapi import FastAPI
from src.api.router import router  # Ensure this points to the updated router.py
import logging

# Logging configuration
logging.basicConfig(level=logging.DEBUG)

# Define the API app
app = FastAPI(
    openapi_url="/hyperlink/api/openapi.json",
    docs_url="/hyperlink/api/docs",
    redoc_url="/hyperlink/api/redoc",
)

# Include the main router
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("api_main:app", reload=True, host="0.0.0.0", port=8000)
