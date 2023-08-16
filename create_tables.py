from connect import engine, SQLModel
from sqlalchemy_utils import create_database, database_exists

if not database_exists(engine.url):
    create_database(engine.url)

SQLModel.metadata.drop_all(engine)
SQLModel.metadata.create_all(engine)
