import sqlmodel
import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.encoders import jsonable_encoder

from hyperlink_data_models.pod_data import (
    PodData,
    PodDataCreate,
    PodDataRead,
    BrakingDataResponse,
    PropulsionDataResponse,
    StructureDataResponse
)
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
                # TODO: look into below, it killed the ws connection
                # await websocket_handler.broadcast_message(f"New pod data created: {pod_data_serialized}")

            except json.JSONDecodeError:
                await websocket_handler.send_json(websocket, {"error": "Invalid JSON received"})
    except WebSocketDisconnect:
        logger.info("Client disconnected")
        await websocket_handler.disconnect(websocket)
    except Exception as e:
        logger.error(f"Error in WebSocket connection: {str(e)}")


@router.get(
    path=f"/{API_VERSION}/{ENDPOINT_NAME}/read_pod_data",
    response_model=list[PodDataRead]
)
def read_pod_data(n: int = 100) -> list[PodDataRead]:
    """
    Fetches the last n data points from the pod data table (all columns)

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


@router.get(
    path=f"/{API_VERSION}/{ENDPOINT_NAME}/braking",
    response_model=list[BrakingDataResponse]
)
def get_braking_data(n: int = 100) -> list[BrakingDataResponse]:
    """
    Get the last n datapoints from the PodData table from column temperature_celsius_braking.
    """
    try:
        statement = (
                    sqlmodel.select(PodData.temperature_celsius_braking, PodData.brake_version)
                    .order_by(PodData.time)
                    .limit(n)
        )

        with sqlmodel.Session(engine) as session:
            data = session.exec(statement).all()

        logger.debug("Encountered no errors")

        # Reverse to maintain chronological order
        return list(reversed([row for row in data if row is not None]))  # TODO: not sure about this tbh

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return []


@router.get(
    path=f"/{API_VERSION}/{ENDPOINT_NAME}/propulsion",
    response_model=list[PropulsionDataResponse]
)
def get_propulsion_data(n: int = 100) -> list[PropulsionDataResponse]:
    """
    """
    try:
        statement = (
                    sqlmodel.select(
                        PodData.temperature_celsius_propulsion_1,
                        PodData.temperature_celsius_propulsion_2,
                        PodData.acceleration_m_per_s2_propulsion,
                        PodData.speed_m_per_s_propulsion,
                        PodData.rpm_propulsion,
                        PodData.propulsion_version
                    )
                    .order_by(PodData.time)
                    .limit(n)
        )

        with sqlmodel.Session(engine) as session:
            data = session.exec(statement).all()

        logger.debug("Encountered no errors")

        # Reverse to maintain chronological order
        return list(reversed([row for row in data if row is not None]))  # TODO: not sure about this tbh

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return []


@router.get(
    path=f"/{API_VERSION}/{ENDPOINT_NAME}/structures",
    response_model=list[StructureDataResponse]
)
def get_structures_data(n: int = 100) -> list[StructureDataResponse]:
    """
    """
    try:
        statement = (
                    sqlmodel.select(
                        PodData.temperature_celsius_structures,
                        PodData.vibration_structures,
                        PodData.deformation_structures,
                        PodData.structure_version
                    )
                    .order_by(PodData.time)
                    .limit(n)
        )

        with sqlmodel.Session(engine) as session:
            data = session.exec(statement).all()

        logger.debug("Encountered no errors")

        # Reverse to maintain chronological order
        return list(reversed([row for row in data if row is not None]))  # TODO: not sure about this tbh

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return []
