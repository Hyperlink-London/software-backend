import sqlmodel
from fastapi import HTTPException
from starlette.status import HTTP_201_CREATED
from sqlalchemy.exc import SQLAlchemyError
from hyperlink_data_models.test import Test, TestCreate  # Adjust import paths as needed
from hyperlink_api.database import engine  # Import the engine from your database file
from hyperlink_api._application import app
from . import API_VERSION

ENDPOINT_NAME = __name__.split('.')[-1]


@app.post(f"/{API_VERSION}/{ENDPOINT_NAME}/test/", response_model=Test, status_code=HTTP_201_CREATED)
async def create_test(test: TestCreate):
    """
    Endpoint to create a new record in the Test table.
    """
    new_test = Test(id=test.id, name=test.name)

    with sqlmodel.Session(engine) as session:
        session.add(new_test)

        try:
            session.commit()
            session.refresh(new_test)  # Refresh to get the newly created data back
        except SQLAlchemyError as e:
            session.rollback()  # Rollback in case of an error
            raise HTTPException(status_code=500, detail=f"Error inserting test: {str(e)}")

    return new_test