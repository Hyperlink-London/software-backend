from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4

import sqlmodel
from sqlalchemy.dialects.postgresql import UUID as SQLAlchemyUUID
from sqlalchemy.dialects.postgresql import JSON as SQLAlchemyJSON


class CommandStatus(str, Enum):
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
    FAILED = "FAILED"


class CommandBase(sqlmodel.SQLModel):
    """
    Class to save requested command with a state. Base class to inherit from it in other models.
    """
    ESP_ID: str


class Command(CommandBase, sqlmodel.SQLModel, table=True):
    """
    Class to save requested command with a state.
    """
    uuid: UUID | None = sqlmodel.Field(default_factory=uuid4, sa_column=sqlmodel.Column(SQLAlchemyUUID, primary_key=True))

    # experiment
    ESP_ID: str = sqlmodel.Field(
        index=True,
    )

    data: dict = sqlmodel.Field(sa_column=sqlmodel.Column(SQLAlchemyJSON))
    status: CommandStatus | None = sqlmodel.Field(
        default=CommandStatus.IN_PROGRESS,
        sa_column=sqlmodel.Column(
            sqlmodel.Enum(CommandStatus),
            nullable=False,
        ),
    )
    failed_reason: str | None = None
    created_at: datetime | None = sqlmodel.Field(
        sa_column=sqlmodel.Column(
            sqlmodel.DateTime(timezone=True),
            nullable=False
        ),
        default_factory=datetime.utcnow,
    )
    updated_at: datetime | None = sqlmodel.Field(
        sa_column=sqlmodel.Column(
            sqlmodel.DateTime(timezone=True),
            nullable=False
        ),
        default_factory=datetime.utcnow,
    )
    retry_counter: int = 0


class CommandCreate(CommandBase):
    """
    Model for creating a new command record.
    """
    data: dict


class CommandRead(CommandBase):
    """
    Model for updating existing Command records with a new status.
    """
    uuid: UUID
    status: CommandStatus = CommandStatus.IN_PROGRESS
    data: dict
    failed_reason: str | None
    created_at: datetime
    updated_at: datetime
