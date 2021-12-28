from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Server(Base):
    __tablename__ = 'example_server'

    id = Column(Integer, primary_key=True)

    ip = Column(String, nullable=False)
    hostname = Column(String, nullable=False)
    power_on = Column(Boolean, server_default='False')

