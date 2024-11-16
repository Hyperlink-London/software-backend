from typing import List
from fastapi import WebSocket, WebSocketDisconnect
from src.core.logger import logger


class WebSocketHandler:
    """
    A class to manage WebSocket connections and broadcasting messages.
    """

    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect_websocket(self, websocket: WebSocket):
        """
        Establishes a WebSocket connection and manages its lifecycle.

        Parameters:
            websocket: The WebSocket connection to be managed.
        """
        await self.add_connection(websocket)
        try:
            while True:
                # Keep the connection open, optionally listen for pings or messages
                await websocket.receive_text()  # Simply keep the connection alive
        except WebSocketDisconnect:
            self.remove_connection(websocket)
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            await websocket.send_json({"error": str(e)})

    async def add_connection(self, websocket: WebSocket):
        """
        Adds a WebSocket connection to the active connections list.
        """
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"New WebSocket connection added: {websocket.client}")

    def remove_connection(self, websocket: WebSocket):
        """
        Removes a WebSocket connection from the active connections list.
        """
        self.active_connections.remove(websocket)
        logger.info(f"WebSocket connection removed: {websocket.client}")

    async def broadcast_message(self, message: str):
        """
        Sends a message to all connected WebSocket clients.
        """
        for connection in self.active_connections:
            await connection.send_text(message)
