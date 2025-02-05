from datetime import datetime
from typing import Optional

import sqlmodel


class PodStateBase(sqlmodel.SQLModel):
    """
    Base class for pod state models, defining pod states
    """
    breaking_state: Optional[str] = None
    propulsion_state: Optional[str] = None
    structures_state: Optional[str] = None
    pod_state: Optional[str] = None


class PodState(PodStateBase, table=True):
    """
    Model representing a table of pod state in the database.

    Inherits attributes from PodStateBase and adds specific data attributes.

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


class PodStateCreate(PodStateBase):
    """
    Model for creating new pod state records.

    Inherits attributes from PodStateBase.

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


class PodStateRead(PodStateBase):
    """
    Model for reading pod state records.

    Inherits attributes from PodStateBase and adds additional attributes for reading.

    Attributes:
        time: Timestamp for the state record.
    """
    time: datetime


class PodStateUpdate(sqlmodel.SQLModel):
    """
    Model for updating existing pod state records.
    """
    pass
