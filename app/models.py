
from sqlalchemy.sql.expression import column, null, text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .db import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

class PostModelORM(Base):
    __tablename__= "Post"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="True", nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    UserID = Column(Integer, ForeignKey("User.id", ondelete="CASCADE"),nullable=False)
    user = relationship("UserModelORM")

class UserModelORM(Base):
    __tablename__ = 'User'

    email= Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False,)
    id = Column(Integer, primary_key=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class FavoriteModelORM(Base):
    __tablename__ = "Favorite"
    UserID = Column(Integer, ForeignKey("User.id", ondelete="CASCADE"), primary_key=True)
    PostID = Column(Integer, ForeignKey("Post.id", ondelete="CASCADE"), primary_key=True)