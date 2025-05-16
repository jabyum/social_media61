from fastapi import FastAPI

app = FastAPI(docs_url="/")
from api.photo_api.photo import photo_router
app.include_router(photo_router)
# uvicorn main:app --reload