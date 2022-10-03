from email.policy import default
from sqlalchemy import Column, Integer, String, DateTime,JSON
# from sqlalchemy.orm import relationship
from dbsetting2 import Base
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class ReportSetting(Base):
  __tablename__ = "report_setting"

  uuid = Column(String, primary_key=True,default=generate_uuid)
  name = Column(String(255), nullable=False)
  template_file = Column(String(255))
  settings = Column(JSON)
  created_at = Column(DateTime)
  updated_at = Column(DateTime)


