from fastapi import FastAPI
from database import Base, engine
from signup_router import router as signup_router
from login_router import router as login_router

Base.metadata.create_all(bind=engine)
print("Tables created successfully!")

app = FastAPI()
app.include_router(signup_router)
app.include_router(login_router)
