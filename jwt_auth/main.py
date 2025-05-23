from fastapi import (FastAPI, Request,
                     Response, HTTPException,
                     Depends)
from authx import AuthX, AuthXConfig
from authx.exceptions import AuthXException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from datetime import timedelta

app = FastAPI(docs_url="/")
# объект для конфигурация JWT (JavaScript Web Token)
config = AuthXConfig()
# время действия токена
config.JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=1)
# создаем ключ
config.JWT_SECRET_KEY = "MY_SECRET_KEY2213312"
# определяем где будет храниться токен
config.JWT_TOKEN_LOCATION = ["cookies"]
# называем название нашего куки-файла
config.JWT_ACCESS_COOKIE_NAME = "my_projects_token"
# объект для генерации токенов
security = AuthX(config=config)
# обработка ошибки связанной с JWT
@app.exception_handler(AuthXException)
async def jwt_error(request: Request, exc: AuthXException):
    return JSONResponse(status_code=401, content={"message": "вы не авторизованы\n"
                                                             "Войдите в систему"})
# схема для получения информации login
class UserLoginSchema(BaseModel):
    username: str
    password: str
#временная бд
database = ["botir", "admin123"]
@app.post("/login")
async def login_with_jwt(credentials: UserLoginSchema,
                         response: Response):
    if (credentials.username == database[0] and  #идентификация
            credentials.password == database[1]): # аутентификация
        # авторизация
        # генерируем JWT
        token = security.create_access_token(uid='101')
        # сохраняем токен в куки пользователя
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME,
                            token)
        return {"access_token": token}
    raise HTTPException(status_code=401,
                          detail={"ошибка": "неправильный логин или пароль"})

# функция с проверкой токена
@app.get("/test", dependencies=[Depends(security.access_token_required)])
async def test(request: Request):
    return "ok"
# функция для выхода из аккаунта
@app.get("/logout",  dependencies=[Depends(security.access_token_required)])
async def logout(response: Response, request: Request):
    response.delete_cookie(config.JWT_ACCESS_COOKIE_NAME)
    return {"message": "Вы успешно вышли из аккаунта"}
