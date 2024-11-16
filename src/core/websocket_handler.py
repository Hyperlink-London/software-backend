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

        Parameters:
            websocket: The WebSocket connection to be managed.
        """
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"Client connected. Total connections: {len(self.active_connections)}")

    async def disconnect(self, websocket: WebSocket):
        """
        Removes a WebSocket connection from the active connections list.
        """
        self.active_connections.remove(websocket)
        logger.info(f"Client disconnected. Total connections: {len(self.active_connections)}")

    async def broadcast(self, message: str):
        """
        Sends a message to all connected WebSocket clients.
        """
        for connection in self.active_connections:
            await connection.send_text(message)
