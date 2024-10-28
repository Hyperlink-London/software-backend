"""
Write pod data into the poddata table.
"""
import sqlmodel

from hyperlink_api.logger import logger
from hyperlink_api._application import app
from hyperlink_api.database import engine
from . import API_VERSION

from hyperlink_data_models.pod_data import (
    PodData,
    PodDataCreate,
    PodDataRead,
)

ENDPOINT_NAME = __name__.split('.')[-1]


@app.post(
    path=f"/{API_VERSION}/{ENDPOINT_NAME}/create_pod_data",
    response_model=PodData
)
def create_microcontroller_data(data: PodDataCreate) -> PodData:
    """
    Creates a new pod data entry in the database.

    Parameters:
        data: The data to be added, encapsulated in a PodDataCreate object.

    Returns:
        The newly created PodData object.
    """
    try:
        with sqlmodel.Session(engine) as session:
            data = PodData.from_orm(data)
            session.add(data)
            session.commit()
            session.refresh(data)
            return data
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return PodData()


@app.get(
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
