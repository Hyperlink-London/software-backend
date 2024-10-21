from sqlmodel import SQLModel, create_engine

# without these imports, the tables do not get created (even though the imports are not used in the script)
# will add here

DEV = False

PRODUCTION_DATABASE_URL = ''
TEST_DATABASE_URL = ''

# database_url = TEST_DATABASE_URL if DEV is True else PRODUCTION_DATABASE_URL
database_url = PRODUCTION_DATABASE_URL

engine = create_engine(
    url=database_url,
    echo=True,
)

SQLModel.metadata.create_all(engine)
SQLModel.metadata.reflect(engine)
