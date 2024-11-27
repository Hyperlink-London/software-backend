from sqlmodel import SQLModel, create_engine
from dotenv import load_dotenv
import os

# without these imports, the tables do not get created (even though the imports are not used in the script)
from hyperlink_data_models.pod_data import PodData
from hyperlink_data_models.pod_states import PodState
from hyperlink_data_models.pod_battery import PodBattery

# Determine the root directory of the project (one level up from current directory)
current_script_dir = os.path.dirname(os.path.abspath(__file__))
project_root_dir = os.path.dirname(current_script_dir)

# Path to the .env file in the root directory
env_file_path = os.path.join(project_root_dir, '.env')

# Load the environment variables from the .env file
load_dotenv(dotenv_path=env_file_path)

DEV = False

PRODUCTION_DATABASE_URL = os.getenv("PRODUCTION_DATABASE_URL")
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

# database_url = TEST_DATABASE_URL if DEV is True else PRODUCTION_DATABASE_URL
database_url = PRODUCTION_DATABASE_URL

engine = create_engine(
    url=database_url,
    echo=True,
)

SQLModel.metadata.create_all(engine)
SQLModel.metadata.reflect(engine)
