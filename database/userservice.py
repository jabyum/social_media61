from database import get_db
from database.models import *
from sqlalchemy import or_
# 1- регистрация
def registration_db(nickname, email, phone_number, password, name, surname, birthdate, city):
        with next(get_db()) as db:
            user = db.query(User).filter(User.nickname == nickname).first()
            if user:
                return {
                    "message": "Такой юзернейм уже существует"
                }
            user = db.query(User).filter(User.email == email).first()
            if user:
                return {
                    "message": "Такой email уже существует"
                }

            user = db.query(User).filter(User.phone_number == phone_number).first()
            if user:
                return {
                    "message": "Такой номер телефона уже существует"
                }

            user = User(username=nickname, phone_number=phone_number, email=email, password=password,
                        name=name, surname=surname, birthdate=birthdate, city=city)
            db.add(user)
            db.commit()
            db.refresh(user)
            return user.id


def registration2_db(nickname, email, phone_number, password, name, surname, birthdate, city):
    with next(get_db()) as db:
        user = db.query(User).filter(User.nickname == nickname).first()
        text = ""
        if user:
            text += "- юзернейм\n"
        user = db.query(User).filter(User.email == email).first()
        if user:
            text += "-почта\n"
        user = db.query(User).filter(User.phone_number == phone_number).first()
        if user:
            text += "-номер\n"
        if user:
            return text + "уже занят(-ы)"
        user = User(username=nickname, phone_number=phone_number, email=email, password=password,
                    name=name, surname=surname, birthdate=birthdate, city=city)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user.id



# 2- вход в аккаунт (по нику, номеру или почте)
def login_db(username, phone_number, email, password):
    with next(get_db()) as db:
        user = db.query(User).filter(or_(User.username == username
                                         , User.phone_number == phone_number
                                         , User.email == email)).first()
        if user:
            if not user.password == password:
                return {
                    "message":"Неверный пароль"
                }
            return {
                "message":user.id
            }
# 3- Изменение информации профиля
# 4- Получение профиль
# 5- Удаление профиля
