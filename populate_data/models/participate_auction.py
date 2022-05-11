from .base import Base
from sqlalchemy import Column, VARCHAR, BIGINT, REAL, ForeignKey

class Participate_Auction(Base):
    __tablename__ = 'participate_auction'
    email = Column(VARCHAR,ForeignKey("users.email"),primary_key=True)
    good_id = Column(BIGINT,ForeignKey("second_hand_goods.good_id"),primary_key=True)
    price = Column(REAL)
    