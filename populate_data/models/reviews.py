from .base import Base
from datetime import datetime
from sqlalchemy import Column, VARCHAR, BIGINT, TIMESTAMP, TEXT, ForeignKey

class Reviews(Base):
    __tablename__ = 'reviews'
    review_id = Column(BIGINT, autoincrement=True, nullable=False, primary_key=True)
    content = Column(TEXT)
    time = Column(TIMESTAMP, default=datetime.now)
    writer_email = Column(VARCHAR, ForeignKey("users.email"), nullable = False)
    receiver_email = Column(VARCHAR, ForeignKey("users.email"), nullable = False)
    