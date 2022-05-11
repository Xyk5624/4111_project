from .base import Base
from datetime import datetime
from sqlalchemy import Column, VARCHAR, BIGINT, INTEGER, REAL, TIMESTAMP, ForeignKey

class Orders(Base):
    __tablename__ = 'orders'
    order_id = Column(BIGINT, autoincrement=True, nullable=False, primary_key=True)
    total_price = Column(REAL)
    time = Column(TIMESTAMP, default=datetime.now)
    email = Column(VARCHAR, ForeignKey("users.email"), nullable = False)
    good_id = Column(BIGINT, ForeignKey("second_hand_goods.good_id"), nullable=False)
    