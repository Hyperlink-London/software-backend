import sqlmodel
import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.encoders import jsonable_encoder

from hyperlink_data_models.pod_data import PodData, PodDataCreate
from src.core.websocket_handler import WebSocketHandler
from src.core.database import engine
from src.core.logger import logger
from . import API_VERSION

ENDPOINT_NAME = __name__.split('.')[-1]

router = APIRouter()
websocket_handler = WebSocketHandler()


@router.websocket("/ws/create_pod_data")
async def websocket_create_pod_data(websocket: WebSocket):
    """
    WebSocket endpoint that handles connections using the WebSocketHandler.
    """
    await websocket_handler.connect(websocket)
    logger.info("WebSocket connection managed by WebSocketHandler")
    try:
        while True:
            try:
                # Receive JSON data using the handler
                data = await websocket_handler.receive_json(websocket)
                logger.info(f"Received data: {data}")

                # Process the received data
                pod_data_create = PodDataCreate(**data)
                with sqlmodel.Session(engine) as session:
                    pod_data = PodData.from_orm(pod_data_create)
                    session.add(pod_data)
                    session.commit()
                    session.refresh(pod_data)

                # Serialize the pod_data with JSON-compatible encoding
                pod_data_serialized = jsonable_encoder(pod_data)

                # Send the JSON-serialised data to the client
                await websocket.send_json({
                    "message": "Pod data created successfully",
                    "data": pod_data_serialized,
                })
                await websocket_handler.broadcast_message(f"New pod data created: {pod_data_serialized}")

            except json.JSONDecodeError:
                await websocket_handler.send_json(websocket, {"error": "Invalid JSON received"})
    except WebSocketDisconnect:
        logger.info("Client disconnected")
        await websocket_handler.disconnect(websocket)
    except Exception as e:
        logger.error(f"Error in WebSocket connection: {str(e)}")


@router.get(
    path=f"/{API_VERSION}/{ENDPOINT_NAME}/read_pod_data",
    response_model=list[PodData]
)
def read_pod_data(n: int = 100) -> list[PodData]:
    """
    Fetches the last n data points from the pod data table.

    Parameters:
        n: The number of data points to retrieve, 100 by default.

    Returns:
        A list of PodDataRead objects, containing the retrieved data.
    """
    try:
        statement = sqlmodel.select(PodData) \
            .order_by(PodData.time) \
            .limit(n)

        with sqlmodel.Session(engine) as session:
            data = session.exec(statement).all()
            logger.debug(f"encountered no errors")
            return [PodData.from_orm(row) for row in data]
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return []
