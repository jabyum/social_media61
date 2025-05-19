from database import Base
from sqlalchemy import Column, ForeignKey, String, Integer, Boolean, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
import pytz

tashkent_tz = pytz.timezone("Asia/Tashkent")

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nickname = Column(String, unique=True)
    email = Column(String, unique=True, nullable=True)
    phone_number = Column(String, unique=True, nullable=True)
    password = Column(String)
    name = Column(String)
    surname = Column(String, nullable=True)
    birthdate = Column(String, nullable=True)
    city = Column(String, nullable=True)
    reg_date = Column(DateTime, default=lambda: datetime.now(tashkent_tz))
    post_fk = relationship("Post", lazy="subquery", back_populates="user_fk", cascade="all, delete-orphan",
                           passive_deletes=True)
class Post(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    text =  Column(String, nullable=True)
    like = Column(Integer, default=0)
    hashtag = Column(String, ForeignKey("hashtag.hashtag_name"))
    reg_date = Column(DateTime, default=lambda: datetime.now(tashkent_tz))
    user_fk = relationship("User", lazy="subquery", back_populates="post_fk")
    hashtag_fk = relationship("Hashtag", lazy="subquery")

class Comments(Base):
    __tablename__ ="comments"
    id=Column(Integer,primary_key=True,autoincrement=True)
    text = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("post.id"))
    data_upload = Column(DateTime,default= lambda :datetime.now(tashkent_tz))
    likes = Column(Integer, default=0)
    answers = Column(Integer, nullable=True)
    user_fk = relationship("User", lazy="subquery")
    post_fk = relationship("Post", lazy="subquery")
class Hashtag(Base):
    __tablename__ = "hashtag"
    id = Column(Integer, primary_key = True, autoincrement = True  )
    hashtag_name = Column(String, unique=True)
    hashtag_post_date = Column(DateTime, default = lambda  : datetime.now(tashkent_tz))
class Photo(Base):
    __tablename__ = "photo"
    id = Column(Integer, primary_key = True , autoincrement = True)
    post_id = Column(Integer, ForeignKey("post.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    photo_path = Column(String, unique=True)
    post_fk = relationship("Post", lazy="subquery")
    user_fk = relationship("User", lazy = "subquery")