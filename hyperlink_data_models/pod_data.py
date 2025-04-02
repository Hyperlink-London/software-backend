from sqlalchemy.dialects.postgresql import UUID as SQLAlchemyUUID
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional


import sqlmodel


class PodDataBase(sqlmodel.SQLModel):
    """
    Base class for pod data models, defining common sensor attributes.
    """
    # Braking data
    temperature_celsius_braking: Optional[float] = None

    # Propulsion data
    temperature_celsius_propulsion_1: Optional[float] = None
    temperature_celsius_propulsion_2: Optional[float] = None
    acceleration_m_per_s2_propulsion: Optional[float] = None
    speed_m_per_s_propulsion: Optional[float] = None
    rpm_propulsion: Optional[float] = None

    # Structures data
    temperature_celsius_structures: Optional[float] = None
    vibration_structures: Optional[float] = None  # TODO: find out what this is measuring and in what units
    deformation_structures: Optional[float] = None  # TODO: find out what this is measuring and in what units

    # Misc data
    # TODO: fix this, its causing an error which kills the ws connection...
    # uuid: UUID | None = sqlmodel.Field(default_factory=uuid4, sa_column=sqlmodel.Column(SQLAlchemyUUID, primary_key=False))  # This is to identify each pud run

    # component versions
    brake_version: Optional[str] = None
    propulsion_version: Optional[str] = None
    structure_version: Optional[str] = None
    pod_version: Optional[str] = None

    run_id: Optional[str] = None #Todo: Convert to UUID
    demo: Optional[float] = None # Testing column for demo purposes


class PodData(PodDataBase, table=True):
    """
    Model representing a table of pod data in the database.

    Inherits attributes from PodDataBase and adds specific data attributes.

    Attributes:
        id: (Optional) Primary key for the database record.
        time: Timestamp for the data record, including timezone information.
    """

    id: int | None = sqlmodel.Field(primary_key=True, default=None)
    time: datetime = sqlmodel.Field(
        sa_column=sqlmodel.Column(
            sqlmodel.DateTime(timezone=True),
            nullable=False
        ),
        default_factory=datetime.utcnow,
    )


class PodDataCreate(PodDataBase):
    """
    Model for creating new pod data records.

    Inherits attributes from PodDataBase.

    Methods:
        from_sensor_output_string: Class method to create an instance from a sensor output string.
    """

    @classmethod
    def from_sensor_output_string(cls, string: str):
        data_split = string.split(sep=",")
        sensor_data = {
            pair.split(sep=':')[0]: pair.split(sep=':')[1]
            for pair
            in data_split[1:]
        }
        sensor_data['pod_id'] = data_split[0]
        return cls(**sensor_data)


class PodDataRead(PodDataBase):
    """
    Model for reading pod data records.

    Inherits attributes from PodDataBase and adds additional attributes for reading.

    Attributes:
        time: Timestamp for the data record.
    """
    time: datetime


class PodDataUpdate(sqlmodel.SQLModel):
    """
    Model for updating existing pod data records.
    """
    pass


class BrakingDataResponse(BaseModel):
    """
    DEP
    """
    temperature_celsius_braking: float
    brake_version: str


class PropulsionDataResponse(BaseModel):
    """
    DEP
    """
    temperature_celsius_propulsion_1: float
    temperature_celsius_propulsion_2: float
    acceleration_m_per_s2_propulsion: float
    speed_m_per_s_propulsion: float
    rpm_propulsion: float
    propulsion_version: str


class StructureDataResponse(BaseModel):
    """
    DEP
    """
    temperature_celsius_structures: float
    vibration_structures: float
    deformation_structures: float
    structure_version: str


