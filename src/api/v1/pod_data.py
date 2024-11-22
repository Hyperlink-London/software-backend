import sqlmodel
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.encoders import jsonable_encoder
from src.core.database import engine
from hyperlink_data_models.pod_data import PodData, PodDataCreate
from src.core.logger import logger
from src.core.websocket_handler import WebSocketHandler
import json

router = APIRouter()
websocket_handler = WebSocketHandler()


@router.websocket("/ws")
async def websocket_data_endpoint(websocket: WebSocket):
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



@router.websocket("/ws/create_pod_data")
async def websocket_create_pod_data(websocket: WebSocket):
    """
    WebSocket handler for creating pod data entries.
    """

    await websocket.accept()
    logger.info("WebSocket connection accepted")

    await websocket_handler.add_connection(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            pod_data_create = PodDataCreate(**data)
            with sqlmodel.Session(engine) as session:
                pod_data = PodData.from_orm(pod_data_create)
                session.add(pod_data)
                session.commit()
                session.refresh(pod_data)

            await websocket.send_json({
                "message": "Pod data created successfully",
                "data": pod_data.dict(),
            })
            await websocket_handler.broadcast_message(f"New pod data created: {pod_data.dict()}")

    except WebSocketDisconnect:
        websocket_handler.remove_connection(websocket)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        await websocket.send_json({"error": str(e)})

# TODO: this should NOT be a websocket endpoint, it should be HTTP
@router.websocket("/ws/read_pod_data")
async def websocket_read_pod_data(websocket: WebSocket):
    """
    WebSocket handler for reading pod data entries.
    """
    await websocket_handler.add_connection(websocket)
    try:
        while True:
            # Receive the number of records to fetch from the client
            message = await websocket.receive_text()
            n = int(message) if message.isdigit() else 100

            statement = (
                sqlmodel.select(PodData)
                .order_by(PodData.time)
                .limit(n)
            )

            with sqlmodel.Session(engine) as session:
                data = session.exec(statement).all()
                pod_data_list = [pod_data.dict() for pod_data in data]

            await websocket.send_json({"data": pod_data_list})
    except WebSocketDisconnect:
        websocket_handler.remove_connection(websocket)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        await websocket.send_json({"error": str(e)})