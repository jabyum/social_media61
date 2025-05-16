from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse
import random
import os
from configs import BASE_DIR
from typing import Union, Optional
photo_router = APIRouter(prefix="/file",
                         tags=["Работа с файлами"])
print(BASE_DIR)
@photo_router.post("/add-photo")
async def add_photo(post_id: int | None = None,
                    user_id: int | None = None,
                    photo_file: UploadFile = File(...)):
    # path: путь до папки с файлом/ название_файла.расширение
    # относительный путь до папки с файлами (нежелательный)
    dir_path = "database/photos/"
    id = post_id if post_id else user_id
    name = f"{id}_{random.randint(1, 100000000000000000000)}."
    if photo_file:
        try:
            # получаем расширение файла из названия
            extension = photo_file.filename.split(".")[-1]
            print(os.path.join(BASE_DIR, dir_path+name+extension))
            # создаем пустой файл в нужной директории с нужным расширением
            file_in_project = open(file=os.path.join(BASE_DIR, dir_path+name+extension),
                                   mode="xb")

            # прочитали код файла пользователя
            user_file = await photo_file.read()
            # переписываем код юзера в наш файл
            file_in_project.write(user_file)
            file_in_project.close()
        except Exception as error:
            return {"status": 0, "message": "Не удалось загрузить\n"
                                            f"Ошибка {error}"}
        finally:
            return {"status": 1, "message": "Файл загружен"}

@photo_router.get("/photo")
async def get_photo(file_name):
    file_path = os.path.join(BASE_DIR, f"database/photos/{file_name}")
    all_types = ["image/jpeg", "image/png"]
    try:
        file_type = None
        if file_name.lower().endswith(".jpg") or file_name.lower().endswith(".jpeg"):
            file_type = all_types[0]
        elif file_name.lower().endswith(".png"):
            file_type = all_types[1]
        print(file_type)
        return FileResponse(path=file_path,
                            media_type=file_type,
                            filename=file_name)
    except:
        return "Ошибка"






