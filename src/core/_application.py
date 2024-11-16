"""

- Import from here within the application.
- Access from hyperlink_api:app outside the application

This ensures that v1 are available.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .constants import APPLICATION_NAME

app = FastAPI(title=APPLICATION_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
