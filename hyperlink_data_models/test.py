from sqlmodel import SQLModel, Field

class TestBase(SQLModel):
    """
    Base class for test models, defining common attributes.
    """
    id: str = Field(index=True)
    name: str


class Test(SQLModel, table=True):
    """
    Database model representing a test entity.

    Attributes:
        id: Unique identifier for the test. It is the primary key in the database.
        name: A string representing the name of the test.
    """
    id: str = Field(primary_key=True, index=True)
    name: str


class TestCreate(TestBase):
    """
    Model for creating new test records.
    Inherits attributes from TestBase.
    """
    pass


class TestRead(TestBase):
    """
    Model for reading test records.
    Inherits attributes from TestBase.
    """
    id: str
    name: str | None


class TestUpdate(SQLModel):
    """
    Model for updating existing test records.
    Attributes:
        id: Identifier for the test entity.
    """
    id: str
