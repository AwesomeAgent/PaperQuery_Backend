from fastapi import APIRouter
router = APIRouter()
from core.backend.crud import *
@app.post("/login")
def login_for_access_token(loginrequest: LoginRequest,db: Session = Depends(get_db)):
    user = query_user(db, loginrequest.username)
    if not user or user.password != loginrequest.password:
            return  JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=jsonable_encoder({"status_code": status.HTTP_401_UNAUTHORIZED, "msg": "用户名或密码错误"}),
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"username": loginrequest.username,"lid":user.lid}, expires_delta=access_token_expires
    )
    return {
        "status_code": 200,
        "msg": "登录成功",
        "data":{"access_token": access_token, "token_type": "Bearer","expire":generate_future_timestamp(ACCESS_TOKEN_EXPIRE_MINUTES)}
    }

# 测试登录状态
@app.get("/testlogin")
async def testlogin(token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
    user =await get_current_user(token,db)
    return user