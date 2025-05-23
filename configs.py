import os

# указываем абсолютный путь до папки проекта
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def registration_db(nickname, number, email, password, ):
    with next(get_db()) as db:
        exact_user1 = db.filter_by(User.nickname == nickname, User.phone_number == number, User.email == email)
        if exact_user1:
            return "Error"
        else:
            db.add(nickname=nickname, photo_number=number, email=email, password=password)
            db.commit()
            return f"{nickname} has been added"


def login_db(nickname, number, email, password):
    with next(get_db()) as db:
        exact_user1 = db.filter_by(User.nickname == nickname, User.phone_number == number, User.email == email,
                                   User.password == password)
        if exact_user1:
            return "Успешно"
        else:
            return "Wrong password or nickname"