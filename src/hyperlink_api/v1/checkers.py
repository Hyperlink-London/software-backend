from hyperlink_api.logger import logger
from hyperlink_api._application import app
from hyperlink_api.database import engine
from . import API_VERSION

ENDPOINT_NAME = __name__.split('.')[-1]


@app.get(f"/{API_VERSION}/{ENDPOINT_NAME}/health_check")
def health_check():
    return "active"
