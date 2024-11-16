"""

- Import from here within the application.
- Access from hyperlink_api:app outside the application

This ensures that v1 are available.
"""
from fastapi import FastAPI

from .constants import APPLICATION_NAME

app = FastAPI(title=APPLICATION_NAME)
