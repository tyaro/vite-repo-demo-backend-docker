from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
import pandas 

# mysqlのDBの設定
DATABASE = 'postgresql://%s:%s@%s:%s/%s' % (
  "postgres",
  "postgres",
  "postgres",
  "5432",
  "postgres",
)

ENGINE = create_engine(
  DATABASE,
  encoding = "utf-8",
  echo=False # Trueだと実行のたびにSQLが出力される
)

SessionLocal = sessionmaker(
    autocommit = False,
    autoflush = False,
    bind = ENGINE
  )

# Sessionの作成
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

def main():
  qry = "CREATE FUNCTION refresh_updated_at() RETURNS TRIGGER AS $$ \
        BEGIN \
          IF (TG_OP = 'UPDATE') THEN \
            NEW.updated_at := now(); \
            return NEW; \
          END IF; \
        END; \
        $$ LANGUAGE plpgsql;"

  session.execute(qry)
  qry = 'DROP TABLE IF EXISTS report_setting CASCADE;'
  session.execute(qry)

  qry = 'CREATE TABLE report_setting(  \
          id uuid not null DEFAULT gen_random_uuid(), \
          name VARCHAR(255) NOT NULL, \
          template_file VARCHAR(255), \
          settings JSON, \
          created_at time without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP, \
          updated_at time without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP, \
          CONSTRAINT report_setting_pkey PRIMARY KEY (id)  \
        );'
  session.execute(qry)

  qry = 'CREATE TRIGGER update_row BEFORE UPDATE ON report_setting FOR EACH ROW EXECUTE PROCEDURE refresh_updated_at();'
  session.execute(qry)
  session.commit()
  session.close()


if __name__ == "__main__":
    main()
