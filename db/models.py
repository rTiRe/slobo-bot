from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)

class Meme(Base):
    __tablename__ = 'memes'
    
    uuid = Column(String, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    comment = Column(String)
    photo = Column(String)
    likes = Column(Integer, default=0)
    dislikes = Column(Integer, default=0)
    general = Column(String)

class Basket(Base):
    __tablename__ = 'baskets'
    
    meme_uuid = Column(String, ForeignKey('memes.uuid'), primary_key=True)
    user_uuid = Column(Integer, ForeignKey('users.id'), primary_key=True)
