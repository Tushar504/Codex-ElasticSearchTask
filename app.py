from fastapi import FastAPI, HTTPException
from db import Base, engine
from routers.tasks import router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router, prefix="/api")