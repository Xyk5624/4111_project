from .base import Base
from sqlalchemy import Column, VARCHAR, BIGINT, ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash

class Users(Base):
    __tablename__ = 'users'
    username = Column(VARCHAR)
    password_encrypted = Column(VARCHAR)
    email = Column(VARCHAR, nullable=False, primary_key=True)
    telephone = Column(BIGINT)
    building_name = Column(VARCHAR,ForeignKey("apartment_building.name"))

    @property
    def password(self):
        return self.password_encrypted

    # 设置加密的方法,传入密码,对类属性进行操作
    @password.setter
    def password(self, value):
        self.password_encrypted = generate_password_hash(value)

    # 设置验证密码的方法
    def check_password(self, user_pwd):
        return check_password_hash(self.password_encrypted, user_pwd)

