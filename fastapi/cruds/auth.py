from http.client import HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt,JWTError
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
import os
from models.user import User,getDict
from dbsetting import session
import schemas.user as user_schema


SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOEKN_EXPIRE_MINUTES = 30
REFRESH_TOEKN_EXPIRE_DAYS = 60

pwdContext = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# パスワードのハッシュ化
def getPasswordHash(password):
  return pwdContext.hash(password)

# パスワードの検証
def verifyPassword(plainPassword,hashedPassword):
  return pwdContext.verify(plainPassword,hashedPassword)

# ユーザーの認証
def authenticateUser(db:Session,loginid:str,password:str):
  user = db.query(User).filter_by(loginid=loginid).first()
  if user is None:
    return None
  if not verifyPassword(password,user.password_hash):
    return None
  return user

# Tokenの発行(アクセストークンとリフレッシュトークン)
def createToken(loginid:str,db:Session):
  accessTokenPayload = {
    'token_type':'access_token',
    'exp':datetime.utcnow() + timedelta(minutes=ACCESS_TOEKN_EXPIRE_MINUTES),
    'loginid':loginid,
  }
  refreshTokenPayload = {
    'token_type':'refresh_token',
    'exp':datetime.utcnow() + timedelta(days=REFRESH_TOEKN_EXPIRE_DAYS),
    'loginid':loginid,
  }
  accessToken = jwt.encode(accessTokenPayload, SECRET_KEY, algorithm=ALGORITHM)
  refreshToken = jwt.encode(refreshTokenPayload, SECRET_KEY, algorithm=ALGORITHM)

  result = {
    'access_token': accessToken, 
    'refresh_token': refreshToken, 
    'token_type': 'bearer'}

  try:
    user = db.query(User).filter(User.loginid==loginid).first()
    user.refresh_token = refreshToken
    db.commit()
  except ValueError as e:
    result = {'error':str(e)}

  return result

# Tokenから現在のユーザー取得
def getCurrentUserFromToken(token:str,tokenType:str):
  try:
    payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
    print(tokenType,payload)

    if payload['token_type'] != tokenType:
      raise HTTPException(status_code=401,detail=f'トークンタイプ不一致')

    loginid = payload['loginid']
    user = session.query(User).filter(User.loginid==loginid).first()
    dbtoken = jwt.decode(user.refresh_token,SECRET_KEY,algorithms=[ALGORITHM])
    print('database',dbtoken,payload)
    
    if tokenType=='refresh_token' and user.refresh_token != token:
      raise HTTPException(status_code=401, detail='リフレッシュトークン不一致')

  except ValueError as e :
      raise HTTPException(status_code=401, detail=str(e))
  
  return user


async def getCurrentUser(token: str = Depends(oauth2_scheme)):
    return getCurrentUserFromToken(token, 'access_token')


async def getCurrentUserWithRefreshToken(token: str = Depends(oauth2_scheme)):
    return getCurrentUserFromToken(token, 'refresh_token')