from typing import List
from fastapi import WebSocket, WebSocketDisconnect
from src.core.logger import logger


class WebSocketHandler:
    """
    A class to manage WebSocket connections and broadcasting messages.
    """

    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """
        Establishes a WebSocket connection and manages its lifecycle.
        """
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"Client connected. Total connections: {len(self.active_connections)}")

    async def disconnect(self, websocket: WebSocket):
        """
        Removes a WebSocket connection from the active connections list.
        """
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info(f"Client disconnected. Total connections: {len(self.active_connections)}")

    async def send_json(self, websocket: WebSocket, message: dict):
        """
        Sends a JSON message to a specific WebSocket connection.
        """
        await websocket.send_json(message)

    async def receive_json(self, websocket: WebSocket) -> dict:
        """
        Receives a JSON message from a specific WebSocket connection.
        """
        return await websocket.receive_json()

    async def broadcast(self, message: str):
        """
        Sends a message to all connected WebSocket clients.
        """
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                logger.error(f"Failed to send message to a client: {str(e)}")