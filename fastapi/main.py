from fastapi import FastAPI,Request,Depends
from starlette.middleware.cors import CORSMiddleware 
from routers import user,auth,report_setting
from dbsetting import getDb,session
from schemas.user import UserCreateRequest
import cruds.user as user_crud
import hashlib

app = FastAPI(root_path="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,   # 追記により追加
    allow_methods=["*"],      # 追記により追加
    allow_headers=["*"]       # 追記により追加
)


@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(report_setting.router)


def main():
    defaultAdmin = UserCreateRequest(
        loginid = 'admin',
        name = '管理者',
        email = '',
        group = 'system',
        position = '管理者',
        role = 'admin',
        password = hashlib.md5(('admin').encode()).hexdigest(),
    )
    defaultManager = UserCreateRequest(
        loginid = 'manager',
        name = '編集者',
        email = '',
        group = 'system',
        position = '編集者',
        role = 'manager',
        password = hashlib.md5(('manager').encode()).hexdigest(),
    )
    defaultUser = UserCreateRequest(
        loginid = 'user',
        name = 'ユーザー',
        email = '',
        group = 'system',
        position = 'ユーザー',
        role = 'user',
        password = hashlib.md5(('user').encode()).hexdigest(),
    )
    d = user.user_crud.createUser(user=defaultAdmin,db=session)
    d = user.user_crud.createUser(user=defaultManager,db=session)
    d = user.user_crud.createUser(user=defaultUser,db=session)
    print(d)

if __name__ == "__main__":
    main()