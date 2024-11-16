import os
import logging
from logging.handlers import RotatingFileHandler

from datetime import datetime

from src.core.constants import current_script_dir


log_level = logging.WARNING
log_file = f"log-api-{datetime.now().strftime('%d-%m-%Y')}.log"
log_file_dir = os.path.join(current_script_dir, log_file)

logger = logging.getLogger(__name__)
file_handler = RotatingFileHandler(log_file_dir, maxBytes=10485760, backupCount=5)  # 10MB
file_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(module)s - %(funcName)s() - line %(lineno)d - %(levelname)s - %(message)s")
)
logger.addHandler(file_handler)
logger.setLevel(log_level)