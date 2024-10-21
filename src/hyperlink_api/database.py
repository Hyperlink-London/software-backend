"""Handle database connections with a sqlmodel engine.

The engine is created here and reused across the application.
https://sqlmodel.tiangolo.com/tutorial/create-db-and-table/?h=create+engin#create-the-engine
"""
from sqlmodel import create_engine
from dotenv import load_dotenv
import os

from ._utils import dev_mode_active

PRODUCTION_DATABASE_URL = os.getenv("PRODUCTION_DATABASE_URL")
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

database_url = TEST_DATABASE_URL if dev_mode_active() else PRODUCTION_DATABASE_URL

engine = create_engine(
    url=database_url,
    echo=False,  # set to True to see SQL queries
)
