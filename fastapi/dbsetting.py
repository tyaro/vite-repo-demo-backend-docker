from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base


# DBの設定
SQLALCHEMY_DATABASE_URL = 'postgresql://%s:%s@%s:%s/%s' % (
  "postgres",
  "postgres",
  "postgres",
  "5432",
  "system",
)

ENGINE = create_engine(
  SQLALCHEMY_DATABASE_URL,
  echo=False # Trueだと実行のたびにSQLが出力される
)

# Sessionの作成
# ORM実行時の設定。自動コミットするか、自動反映するなど。
SessionLocal = sessionmaker(
    autocommit = False,
    autoflush = False,
    bind = ENGINE
  )

session = scoped_session(SessionLocal)

# modelで使用する
Base = declarative_base()
Base.query = session.query_property()

def getDb():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()