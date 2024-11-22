import sqlmodel
import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.encoders import jsonable_encoder

from hyperlink_data_models.pod_states import PodState, PodStateCreate
from src.core.websocket_handler import WebSocketHandler
from src.core.database import engine
from src.core.logger import logger
from . import API_VERSION

ENDPOINT_NAME = __name__.split('.')[-1]

router = APIRouter()
websocket_handler = WebSocketHandler()


@router.websocket("/ws/create_pod_state")
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
                pod_state_create = PodStateCreate(**data)
                with sqlmodel.Session(engine) as session:
                    pod_state = PodState.from_orm(pod_state_create)
                    session.add(pod_state)
                    session.commit()
                    session.refresh(pod_state)

                # Serialize the pod_data with JSON-compatible encoding
                pod_state_serialized = jsonable_encoder(pod_state)

                # Send the JSON-serialised data to the client
                await websocket.send_json({
                    "message": "Pod state created successfully",
                    "data": pod_state_serialized,
                })
                await websocket_handler.broadcast_message(f"New pod data created: {pod_state_serialized}")

            except json.JSONDecodeError:
                await websocket_handler.send_json(websocket, {"error": "Invalid JSON received"})
    except WebSocketDisconnect:
        logger.info("Client disconnected")
        await websocket_handler.disconnect(websocket)
    except Exception as e:
        logger.error(f"Error in WebSocket connection: {str(e)}")


@router.get(
    path=f"/{API_VERSION}/{ENDPOINT_NAME}/read_pod_states",
    response_model=list[PodState]
)
def read_pod_states(n: int = 100) -> list[PodState]:
    """
    Fetches the last n data points from the pod state table.

    Parameters:
        n: The number of data points to retrieve, 100 by default.

    Returns:
        A list of PodDataRead objects, containing the retrieved data.
    """
    try:
        statement = sqlmodel.select(PodState) \
            .order_by(PodState.time) \
            .limit(n)

        with sqlmodel.Session(engine) as session:
            data = session.exec(statement).all()
            logger.debug(f"encountered no errors")
            return [PodState.from_orm(row) for row in data]
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return []
