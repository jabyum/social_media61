from fastapi import FastAPI
from database import Base, engine
app = FastAPI(docs_url="/")
from api.photo_api.photo import photo_router
Base.metadata.create_all(bind=engine)
app.include_router(photo_router)
# uvicorn main:app --reload