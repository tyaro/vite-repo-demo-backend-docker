from dataclasses import field
from datetime import datetime
from turtle import update
from unicodedata import name
import uuid
from dbsetting2 import ENGINE,session
from typing import Optional
import pandas
from fastapi import File,UploadFile
from sqlalchemy.orm import Session
import os
import shutil
import schemas.report_setting as schemas
import models.report_setting as models
import json

TABLE_NAME = 'report_setting'
UPLOAD_DIR = './template/'

# class ReportSettingModel(BaseModel):
#   ReportName:str
#   TemplateFile:Optional[str]
#   Settings:Optional[str]


class ReportSetting():

  @staticmethod
  def add(data:schemas.ReportSettingBase):
    now = datetime.now()
    newRow = models.ReportSetting(
      name = data.name,
      template_file = data.template_file,
      settings = data.settings,
      created_at = now,
      updated_at = now
    )
    session.add(newRow)
    session.commit()
    qry = session.query(models.ReportSetting).filter(models.ReportSetting.name==data.name)
    df = pandas.read_sql_query(qry.statement,ENGINE)
    df['id'] = df.index
    d = df.astype(str).to_dict(orient='records')
    return d[0]

  @staticmethod
  def save(data:schemas.ReportSetting):
    print('save')
    newData = session.query(models.ReportSetting).filter(models.ReportSetting.uuid==data.uuid).first()
    newData.name = data.name
    newData.template_file = data.template_file
    newData.settings = data.settings
    session.commit()
    qry = session.query(models.ReportSetting).filter(models.ReportSetting.uuid==data.uuid)
    df = pandas.read_sql_query(qry.statement,ENGINE)
    df['id'] = df.index
    d = df.astype(str).to_dict(orient='records')
    createTable(data)
    return d[0]

  @staticmethod
  def delete(data:schemas.ReportSetting):
    qry = session.query(models.ReportSetting).filter(models.ReportSetting.uuid==data.uuid)
    df = pandas.read_sql_query(qry.statement,ENGINE)
    df['id'] = df.index
    d = df.astype(str).to_dict(orient='records')
    res = session.query(models.ReportSetting).filter(models.ReportSetting.uuid==data.uuid).delete()
    print(res)
    session.commit()
    return d[0]

  @staticmethod
  def list(db:Session):
    qry = db.query(models.ReportSetting)
    print(str(qry.statement))
    df = pandas.read_sql_query(qry.statement,ENGINE)
    df['id'] = df.index
    d = df.astype(str).to_dict(orient='records')
    return d

  @staticmethod
  def Upload(file:UploadFile=File(...)):
    if file:
      filename = file.filename
      fileobj = file.file
      upload_dir = open(os.path.join(UPLOAD_DIR, filename),'wb+')
      shutil.copyfileobj(fileobj, upload_dir)
      upload_dir.close()
      return {"アップロードファイル名": filename}
    return {"Error": "アップロードファイルが見つかりません。"}

def createTable(data:schemas.ReportSetting):
  tablename = data.uuid
  qry = 'drop table if exists "' + tablename + '" cascade; \
        create table "' + tablename + '"( \
          uuid uuid NOT NULL DEFAULT gen_random_uuid(), \
          created_at time without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP, \
          updated_at time without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP, '

  settings = json.loads(data.settings)

  cmt = 'comment on table "' + tablename + '" is '+ "'" + data.name + "';"

  for idx,row in enumerate(settings):
    print(row)
    colname = '"' + row['FieldName'] + '"'
    typeData = 'text'
    if row['DataType'] == '数値':
      typeData = 'double precision'
    qry += colname + ' ' + typeData + ','
    cmt += 'comment on column "' + tablename + '".' + colname + ' is ' +"'" + row['DisplayName'] +"';"

  qry += ' CONSTRAINT "' + data.uuid + '_pkey" PRIMARY KEY (uuid));' 
  qry += cmt

  triger = 'CREATE TRIGGER update_row BEFORE UPDATE ON "' + tablename+ '" FOR EACH ROW EXECUTE PROCEDURE refresh_updated_at();'
  qry += triger
  result = ENGINE.execute(qry)
  print(result)

  return result