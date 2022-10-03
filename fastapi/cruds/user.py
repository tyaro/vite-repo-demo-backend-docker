from ast import Delete
from turtle import position
from sqlalchemy.orm import Session,Query
from models.user import User
from cruds.auth import getPasswordHash
from dbsetting import ENGINE
import schemas.user as user_schema
import pandas as pd 
from sqlalchemy import select,delete

# ユーザーのID取得
def getUserLoginId(db:Session,loginid:str):
  return db.query(User).filter_by(loginid=loginid).first()

# ユーザー作成
def createUser(db:Session,user:user_schema.UserCreateRequest):
  passwordHash = getPasswordHash(user.password)
  newUser = User(
    loginid = user.loginid,
    name = user.name,
    email = user.email,
    group = user.group,
    position = user.position,
    role = user.role,
    password_hash = passwordHash,
  )
  db.add(newUser)
  db.commit()
  db.refresh(newUser)
  return newUser

# ユーザーリストの取得
def getUserList(db:Session):
  
  qry = db.query(User).order_by(User.id)
  df = pd.read_sql_query(str(qry.statement),ENGINE)
  #df['id'] = df.index
  d = df.astype(str).to_dict(orient='records')
  return d

# ユーザー作成
def updateUser(db:Session,user:user_schema.UserUpdateRequest):
  if user.id != '':
    id = user.id
    newUser = db.query(User).filter(User.id==id).first()
    newUser.loginid = user.loginid
    newUser.role = user.role
    newUser.name = user.name,
    newUser.email = user.email,
    newUser.group = user.group,
    newUser.position = user.position,
    if user.password != None:
      newUser.password_hash = getPasswordHash(user.password)
    db.commit()
  d = getUser(db,id)
  return d

def getUser(db:Session,id):
  qry = db.query(User).filter(User.id == id)
  df = pd.read_sql_query(qry.statement,ENGINE)
  d = df.astype(str).to_dict(orient='records')[0]
  return d

# ユーザー作成
def deleteUser(db:Session,user:user_schema.UserDeleteRequest):
  user = getUser(db,user.id)
  qry = db.query(User).filter(User.id == user['id']).delete()
  db.commit()
  print(str(qry))
  # df = pd.read_sql_query(qry.statement,ENGINE)
  # d = df.astype(str).to_dict(orient='records')[0]
  # print(d)

  return user