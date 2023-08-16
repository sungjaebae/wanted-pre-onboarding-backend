from sqlmodel import SQLModel, create_engine, Session
import models
engine = create_engine(
    "mysql://root:12341234@localhost/internship", echo=True, )
session = Session(engine)
