"""Handle database connections with a sqlmodel engine.

The engine is created here and reused across the application.
https://sqlmodel.tiangolo.com/tutorial/create-db-and-table/?h=create+engin#create-the-engine
"""
from sqlmodel import create_engine
from dotenv import load_dotenv
import os

from ._utils import dev_mode_active

# Load environment variables
load_dotenv()

# Get the correct database URL depending on the environment
PRODUCTION_DATABASE_URL = os.getenv("PRODUCTION_DATABASE_URL")
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

# Choose the correct database URL based on the development mode
database_url = TEST_DATABASE_URL if dev_mode_active() else PRODUCTION_DATABASE_URL

# Create the SQLModel engine
engine = create_engine(
    url=database_url,
    echo=False,  # set to True to see SQL queries
)