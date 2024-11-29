from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4

import sqlmodel
from sqlalchemy.dialects.postgresql import JSON as SQLAlchemyJSON


class CommandBase(sqlmodel.SQLModel):
    """
    Class to save requested command with a state. Base class to inherit from it in other models.
    """
    ESP_ID: str
    data: dict = sqlmodel.Field(sa_column=sqlmodel.Column(SQLAlchemyJSON))


class Command(CommandBase, sqlmodel.SQLModel, table=True):
    """
    Class to save requested command with a state.
    """
    created_at: datetime | None = sqlmodel.Field(
        sa_column=sqlmodel.Column(
            sqlmodel.DateTime(timezone=True),
            nullable=False
        ),
        default_factory=datetime.utcnow,
    )
    id: int | None = sqlmodel.Field(primary_key=True, default=None)


class CommandCreate(CommandBase):
    """
    Model for creating a new command record.
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


class CommandRead(CommandBase):
    """
    Model for updating existing Command records with a new status.
    """
    data: dict
    created_at: datetime
