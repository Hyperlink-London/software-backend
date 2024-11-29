from fastapi import APIRouter, BackgroundTasks
from uuid import UUID
import sqlmodel
import json
import asyncio
from hyperlink_data_models.command import CommandCreate, CommandRead, Command
from src.core.websocket_handler import websocket_handler
from src.core.database import engine
from src.core.logger import logger
from . import API_VERSION

ENDPOINT_NAME = __name__.split('.')[-1]

router = APIRouter()


async def send_command(command_data: CommandCreate):
    try:
        command_dict = command_data.dict()
        # Assuming command_data includes esp_id
        asyncio.create_task(websocket_handler.broadcast(json.dumps(command_dict)))
    except Exception as e:
        logger.error(f"Failed to send command: {str(e)}")


@router.get("/", response_model=list[CommandRead])
def list_commands(esp_id: str) -> list[CommandRead]:
    pass


@router.get("/{command_uuid}/", response_model=CommandRead)
def get_command(command_uuid: UUID) -> CommandRead:
    pass


@router.post("/execute_command", response_model=dict)
async def execute_command(command_data: CommandCreate) -> Command:
    try:
        with sqlmodel.Session(engine) as session:
            data = Command.from_orm(command_data)
            session.add(data)
            session.commit()
            session.refresh(data)
            await send_command(command_data)
            return data
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return Command()
