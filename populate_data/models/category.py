from .base import Base
from sqlalchemy import Column, VARCHAR

class Category(Base):
    __tablename__ = 'category'
    name = Column(VARCHAR, nullable=False, primary_key=True)