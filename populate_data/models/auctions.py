from .base import Base
from datetime import datetime
from sqlalchemy import Column, BIGINT, INTEGER, REAL, TIMESTAMP, ForeignKey

class Auctions(Base):
    __tablename__ = 'auctions'
    good_id = Column(BIGINT, ForeignKey("second_hand_goods.good_id"), nullable=False,  primary_key=True)
    count_down = Column(INTEGER)
    start_time = Column(TIMESTAMP, default=datetime.now)
    max_price = Column(REAL)
    state = Column(INTEGER)