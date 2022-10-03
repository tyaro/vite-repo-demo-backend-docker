from sqlalchemy import Column, Integer, String, DateTime
# from sqlalchemy.orm import relationship
from dbsetting import Base

class User(Base):
  __tablename__ = "users"

  id = Column(Integer, primary_key=True)
  loginid = Column(String(255), unique=True, nullable=False)
  password_hash = Column(String(255), nullable=False)
  name = Column(String(255), nullable=False)
  email = Column(String(255))
  group = Column(String(255))
  position = Column(String(255))
  role = Column(String(1024))
  refresh_token = Column(String(255))
  created_at = Column(DateTime)
  updated_at = Column(DateTime)


def getDict(user:User):
  return {
    'loginid': user.loginid,
    'name': user.name,
    'email': user.email,
    'group': user.group,
    'position': user.position,
    'role': user.role,
    'created_at': user.created_at,
    'updated_at': user.updated_at,
  }