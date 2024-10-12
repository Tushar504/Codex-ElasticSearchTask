from fastapi import FastAPI, HTTPException
from db import Base, engine


Base.metadata.create_all(bind=engine)

app = FastAPI()