from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from cruds.auth import createToken, getCurrentUser, getCurrentUserWithRefreshToken

import schemas.auth as auth_schema
import schemas.user as user_schema
import cruds.auth as auth_crud
from dbsetting import getDb

router = APIRouter()

@router.post('/token', response_model=auth_schema.Token)
async def login(formData: OAuth2PasswordRequestForm = Depends(),db:Session = Depends(getDb)):
  user = auth_crud.authenticateUser(
    db=db,
    loginid=formData.username,
    password=formData.password
  )
  if user is None:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Incorrect username or password",
      headers={"WWW-Authenticate":"Bearer"}
    )
  token = auth_crud.createToken(loginid=user.loginid,db=db)
  return token

@router.get("/RefreshToken",response_model=auth_schema.Token)
async def refreshToken(currentUser:user_schema.User = Depends(getCurrentUserWithRefreshToken),db:Session = Depends(getDb)):
  
  return createToken(loginid=currentUser.loginid,db=db)

@router.get("/user/me",response_model=user_schema.User)
async def readUsersMe(currentUser:user_schema.User = Depends(getCurrentUser)):
  return currentUser
