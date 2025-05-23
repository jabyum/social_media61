from fastapi import FastAPI, Request
from database import Base, engine
from fastapi.responses import JSONResponse
from authx.exceptions import AuthXException
app = FastAPI(docs_url="/")
from api.photo_api.photo import photo_router
Base.metadata.create_all(bind=engine)
app.include_router(photo_router)
# uvicorn main:app --reload
# обработка ошибки связанной с JWT
@app.exception_handler(AuthXException)
async def jwt_error(request: Request, exc: AuthXException):
    return JSONResponse(status_code=401, content={"message": "вы не авторизованы\n"
                                                             "Войдите в систему"})
