from sqlalchemy import Column, Integer, String, func
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Date, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False, unique=True)
    phone_number = Column(String(20), nullable=False, unique=True)
    birthday = Column(Date, nullable=False, default='1900-01-01')
    description = Column(String(1500), nullable=True)
    user_id = Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), default=None)
    user = relationship('User', backref="notes")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column('crated_at', DateTime, default=func.now())
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)
