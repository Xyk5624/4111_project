from .base import Base
from sqlalchemy import Column, VARCHAR, BIGINT, INTEGER, REAL, TIMESTAMP, ForeignKey

class Goods_Category(Base):
    __tablename__ = 'goods_category'
    name = Column(VARCHAR, ForeignKey("category.name"), nullable=False, primary_key=True)
    good_id = Column(BIGINT, ForeignKey("second_hand_goods.good_id"), autoincrement=True, nullable=False, primary_key=True)
    