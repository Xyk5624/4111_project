from .base import Base
from sqlalchemy import Column, VARCHAR, INTEGER

class Apartment_building(Base):
    __tablename__ = 'apartment_building'
    name = Column(VARCHAR, nullable=False, primary_key=True)
    address = Column(VARCHAR)
    zip_code = Column(INTEGER)
    street_name = Column(VARCHAR)
