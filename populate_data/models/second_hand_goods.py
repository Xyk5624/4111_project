from .base import Base
from sqlalchemy import Column, VARCHAR, BIGINT, INTEGER, REAL, ForeignKey

class Second_hand_goods(Base):
    __tablename__ = 'second_hand_goods'
    good_id = Column(BIGINT, autoincrement=True, nullable=False, primary_key=True)
    state = Column(INTEGER)
    price = Column(REAL)
    description = Column(VARCHAR)
    email = Column(VARCHAR, ForeignKey("users.email"))
    image_url = Column(VARCHAR)