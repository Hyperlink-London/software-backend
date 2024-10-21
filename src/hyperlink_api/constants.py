import os
from dotenv import load_dotenv

# load the environment variables from the .env file which should be created in the src/hyperlink_api directory of the project
current_script_dir = os.path.dirname(os.path.abspath(__file__))
env_file_path = os.path.join(current_script_dir, '.env')

# Load the environment variables from the .env file
load_dotenv(dotenv_path=env_file_path)


APPLICATION_HOST = os.getenv("APPLICATION_HOST")
APPLICATION_HOST_DEV = os.getenv("APPLICATION_HOST_DEV")
APPLICATION_PORT = os.getenv("APPLICATION_PORT")
APPLICATION_PORT_DEV = os.getenv("APPLICATION_PORT_DEV")

APPLICATION_NAME = 'hyperlink-api'
DEV_MODE_ENV_VAR_NAME = 'HYPERLINK_API_DEV_MODE'

# TODO: Update this to the correct version after the next release
API_VERSION = "V0.0.1"  # V0.0.1 initial commit
