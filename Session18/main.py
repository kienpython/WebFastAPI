from fastapi import FastAPI
from database import Base, engine
from routers.student import router as st_router
app = FastAPI()
Base.metadata.create_all(bind = engine)

app.include_router(st_router)