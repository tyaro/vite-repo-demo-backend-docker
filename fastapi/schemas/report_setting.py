from pydantic import BaseModel, Field
from typing import Optional

class ReportSettingBase(BaseModel):
  name: str = Field(None, description="レポート名称")
  template_file: str = Field(None, description="テンプレートファイル")
  settings: str = Field(None, description="セッティング")
  created_at: Optional[str] = Field(None,description="作成日時")
  updated_at: Optional[str] = Field(None,description="更新日時")

  class Config:
    orm_mode = True

class ReportSetting(ReportSettingBase):
  id: int
  uuid: str = Field(None, description="uuid")

  class Config:
    orm_mode = True


