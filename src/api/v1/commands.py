from fastapi import APIRouter, BackgroundTasks
from uuid import UUID
import sqlmodel

from hyperlink_data_models.command import CommandCreate, CommandRead, Command
from src.core.websocket_handler import WebSocketHandler
from src.core.database import engine
from src.core.logger import logger
from . import API_VERSION

ENDPOINT_NAME = __name__.split('.')[-1]

router = APIRouter()
websocket_handler = WebSocketHandler()


def send_command(command_data: CommandCreate):
    """
    Function to send a command to the ESP.
    """
    pass


@router.get("/", response_model=list[CommandRead])
def list_commands(esp_id: str) -> list[CommandRead]:
    pass


@router.get("/{command_uuid}/", response_model=CommandRead)
def get_command(command_uuid: UUID) -> CommandRead:
    pass


@router.post("/execute_command", response_model=dict)
def execute_command(command_data: CommandCreate) -> Command:
    try:
        with sqlmodel.Session(engine) as session:
            data = Command.from_orm(command_data)
            session.add(data)
            session.commit()
            session.refresh(data)
            send_command(command_data)
            return data
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return Command()
