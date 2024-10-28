from datetime import datetime
from typing import Optional

import sqlmodel


class PodDataBase(sqlmodel.SQLModel):
    """
    Base class for pod data models, defining common sensor attributes.
    """
    # experiment
    pod_id: str = sqlmodel.Field(  # this will be used to track design iterations
        index=True,
        # foreign_key="pod.id"
    )

    # sensor
    temperature_celsius_brake: Optional[float] = None
    temperature_celsius_propulsion_1: Optional[float] = None
    temperature_celsius_propulsion_2: Optional[float] = None
    rpm: Optional[float] = None
    speed_m_per_s: Optional[float] = None


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
    Model for updating existing microcontroller data records.
    """
    pass
