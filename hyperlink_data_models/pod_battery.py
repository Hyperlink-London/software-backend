from datetime import datetime
from typing import Optional

import sqlmodel


class PodBatteryBase(sqlmodel.SQLModel):
    """
    Base class for pod battery models, defining pod batteries
    """
    pod_battery_percentage: Optional[float] = None
    pod_battery_voltage: Optional[float] = None
    pod_battery_current: Optional[float] = None
    pod_battery_temperature: Optional[float] = None
    run_id: Optional[str] = None #Todo: Convert to UUID


class PodBattery(PodBatteryBase, table=True):
    """
    Model representing a table of pod battery in the database.

    Inherits attributes from PodBatteryBase and adds specific data attributes.

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


class PodBatteryCreate(PodBatteryBase):
    """
    Model for creating new pod battery records.

    Inherits attributes from PodBatteryBase.

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


class PodBatteryRead(PodBatteryBase):
    """
    Model for reading pod battery records.

    Inherits attributes from PodBatteryBase and adds additional attributes for reading.

    Attributes:
        time: Timestamp for the battery record.
    """
    time: datetime


class PodBatteryUpdate(sqlmodel.SQLModel):
    """
    Model for updating existing pod battery records.
    """
    pass
