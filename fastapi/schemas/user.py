from pydantic import BaseModel, Field
from typing import Optional

class UserBase(BaseModel):
  loginid: str = Field(None, description="ログインID")
  name: str = Field(None, description="表示名")
  email: str = Field(None, description="email")
  group: str = Field(None, description="所属")
  position: str = Field(None, description="役職")
  role: str = Field(None,description="権限")
  created_at: Optional[str] = Field(None,description="作成日時")
  updated_at: Optional[str] = Field(None,description="更新日時")

  class Config:
    orm_mode = True

class User(UserBase):
  id: int

  class Config:
    orm_mode = True

class UserCreateRequest(UserBase):
  password: str = Field(None, description="パスワード")

  class Config:
    orm_mode = True
    
class UserUpdateRequest(UserBase):
  password: str = Field(None, description="パスワード")
  id: int = Field(None,description="id")

  class Config:
    orm_mode = True

class UserDeleteRequest(BaseModel):
  id: int = Field(None,description="id")

  class Config:
    orm_mode = True
