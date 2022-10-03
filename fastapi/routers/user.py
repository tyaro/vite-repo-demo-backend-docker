from unittest import result
from fastapi import APIRouter,Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from dbsetting import getDb
import schemas.user as user_schema
import cruds.user as user_crud
import cruds.auth as auth_crud

router = APIRouter()

@router.post('/user/create',response_model=user_schema.User)
def createUser(user:user_schema.UserCreateRequest,db:Session = Depends(getDb)):
  dbUser = user_crud.getUserLoginId(db,user.loginid)
  if dbUser:
    raise HTTPException(status_code=400,detail="LoginId already exists")
  try:
    newUser = user_crud.createUser(db,user)
  except ValueError as e:
    raise HTTPException(status_code=400,detail="Error CreateUser " + str(e))
  return newUser.__dict__

@router.get('/user/info/{loginid}',response_model=user_schema.User)
def getUser(loginid:str,db:Session = Depends(getDb)):
  dbUser = user_crud.getUserLoginId(db,loginid)
  if dbUser is None:
    raise HTTPException(status_code=400,detail = "User not Found")
  return dbUser.__dict__

@router.get('/user/list',response_model=List[user_schema.User])
def getUserList(db:Session = Depends(getDb),token: str = Depends(auth_crud.oauth2_scheme)):
  # current_user = auth_crud.getCurrentUser(db=db,token=token)
  dbUsers = user_crud.getUserList(db)
  if dbUsers is None:
    raise HTTPException(status_code=400,detail = "User not Found")
  return dbUsers

@router.post('/user/save',response_model=user_schema.User)
def updateUser(user:user_schema.UserUpdateRequest,db:Session = Depends(getDb)):
  try:
    newUser = user_crud.updateUser(db,user)
  except ValueError as e:
    raise HTTPException(status_code=400,detail="Error CreateUser " + str(e))
  return newUser

@router.post('/user/delete',response_model=user_schema.User)
def deleteUser(user:user_schema.UserDeleteRequest,db:Session = Depends(getDb)):
  try:
    newUser = user_crud.deleteUser(db,user)
  except ValueError as e:
    raise HTTPException(status_code=400,detail="Error CreateUser " + str(e))
  return newUser