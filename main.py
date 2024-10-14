from fastapi import FastAPI
from app.utils import models
from app.utils.database import engine
from app.routes.users import users
from app.routes.auth import login

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {"message": "Welcome home"}


app.include_router(login.router)
app.include_router(users.router)
