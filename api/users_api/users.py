from fastapi import (APIRouter, Request,
                     Response, HTTPException,
                     Depends)
from authx.exceptions import AuthXException
from fastapi.responses import JSONResponse
from api.users_api import UserLoginSchema, RegistrationSchema
from jwt_auth.main import config, security
from database.userservice import *
import re
user_router = APIRouter(prefix="/user", tags=["Пользовательская часть"])
regex_mail = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
def mail_checker(mail):
    if re.match(regex_mail, mail):
        return True
    return False
@user_router.post("/register")
async def registration(info: RegistrationSchema):
    mail_validator = mail_checker(info.email)
    if not mail_validator:
        return {"status": 0, "message": "неправильный формат почты"}
    result = registration_db(**dict(info))
    if result:
        return {"status": 1, "message": result}
    return {"status": 0, "message": "ошибка"}


@user_router.post("/login")
async def login_with_jwt(credentials: UserLoginSchema,
                         response: Response):
    result = login_db(credentials.username, credentials.password)
    if result:
        token = security.create_access_token(uid='101')
        # сохраняем токен в куки пользователя
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME,
                            token)
        return {"access_token": token}
    raise HTTPException(status_code=401,
                          detail={"ошибка": "неправильный логин или пароль"})

# функция с проверкой токена
@user_router.get("/test", dependencies=[Depends(security.access_token_required)])
async def test(request: Request):
    return "ok"
# функция для выхода из аккаунта
@user_router.get("/logout",  dependencies=[Depends(security.access_token_required)])
async def logout(response: Response, request: Request):
    response.delete_cookie(config.JWT_ACCESS_COOKIE_NAME)
    return {"message": "Вы успешно вышли из аккаунта"}
