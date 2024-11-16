import sqlmodel
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
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
    # First, explicitly accept the connection
    await websocket.accept()
    logger.info("WebSocket connection accepted")
    
    try:
        # Then add to the handler's active connections
        websocket_handler.active_connections.append(websocket)
        logger.info(f"Client connected. Total connections: {len(websocket_handler.active_connections)}")
        
        while True:
            data = await websocket.receive_text()
            try:
                json_data = json.loads(data)
                logger.info(f"Received data: {json_data}")
                print(f"Received data: {json_data}")
                response = {
                    "message": "Data received successfully",
                    "received_data": json_data
                }
                await websocket.send_json(response)
            except json.JSONDecodeError:
                await websocket.send_json({"error": "Invalid JSON received"})
    except WebSocketDisconnect:
        logger.info("Client disconnected")
        websocket_handler.active_connections.remove(websocket)
    except Exception as e:
        logger.error(f"Error in WebSocket connection: {str(e)}")
        if websocket in websocket_handler.active_connections:
            websocket_handler.active_connections.remove(websocket)