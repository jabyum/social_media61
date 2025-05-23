from pydantic import BaseModel
# схема для получения информации login
class UserLoginSchema(BaseModel):
    username: str
    password: str
# схема для регистрации
class RegistrationSchema(BaseModel):
    nickname: str
    email: str
    phone_number: str
    password: str
    name: str
    surname: str | None = None
    birthdate: str | None = None
    city: str | None = None
    # # создание по данному шаблону объект для ORM
    # class Config:
    #     from_attributes = True