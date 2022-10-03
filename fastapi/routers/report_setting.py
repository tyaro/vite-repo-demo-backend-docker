from unittest import result
from fastapi import APIRouter,Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from dbsetting2 import getDb
import schemas.report_setting as schema
import cruds.report_setting as crud
import cruds.auth as auth_crud

router = APIRouter()

# レポート設定リスト取得
@router.get('/report/setting/list',response_model=List[schema.ReportSetting])
def getReportSettingList(db:Session = Depends(getDb),token: str = Depends(auth_crud.oauth2_scheme)):
  result = crud.ReportSetting.list(db)
  if result is None:
    raise HTTPException(status_code=400,detail = "Report not Found")
  return result

@router.post('/report/setting/add',response_model=schema.ReportSetting)
def addReportSettingList(data:schema.ReportSettingBase,token: str = Depends(auth_crud.oauth2_scheme)):
  result = crud.ReportSetting.add(data)
  if result is None:
    raise HTTPException(status_code=400,detail = "新規レポート設定の作成に失敗しました")
  return result

@router.post('/report/setting/save',response_model=schema.ReportSetting)
def saveReportSettingList(data:schema.ReportSetting,token: str = Depends(auth_crud.oauth2_scheme)):
  result = crud.ReportSetting.save(data)
  if result is None:
    raise HTTPException(status_code=400,detail = "レポート設定の保存に失敗しました")
  return result

@router.post('/report/setting/delete',response_model=schema.ReportSetting)
def deleteReportSettingList(data:schema.ReportSetting,token: str = Depends(auth_crud.oauth2_scheme)):
  result = crud.ReportSetting.delete(data)
  if result is None:
    raise HTTPException(status_code=400,detail = "新規レポート設定の作成に失敗しました")
  return result