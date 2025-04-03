import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

# # Allow requests from your frontend
# origins = [
#     "http://localhost:5173",  # Your frontend (Vite)
#     "http://127.0.0.1:5173",  # Sometimes Vite uses this
#     "http://0.0.0.0:5173"     # If accessing via network
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows listed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)
# Include the main router
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("api_main:app", reload=True, host="0.0.0.0", port=8000)
