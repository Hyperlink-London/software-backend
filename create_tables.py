from sqlmodel import SQLModel, create_engine
from sqlalchemy.exc import OperationalError
import os

# Import the Test model
from hyperlink_data_models.test import Test
from hyperlink_data_models.pod_data import PodData

# Load the environment variables
database_url = os.getenv("PRODUCTION_DATABASE_URL")

# Create the engine
engine = create_engine(database_url, echo=True)


def create_tables():
    try:
        # Try to connect to the database
        with engine.connect() as conn:
            print("Database connection established.")
            # Create tables if they don't exist
            SQLModel.metadata.create_all(engine)
            print("Tables created or already exist.")
    except OperationalError:
        print("Error: Could not connect to the database. Make sure PostgreSQL is running.")


if __name__ == "__main__":
    create_tables()
