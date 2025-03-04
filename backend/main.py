from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from backend.auth_routes import router as auth_router
from backend.database import engine, Base
from backend.api.routers.lodging_router import router as lodging_router


app = FastAPI()

app.include_router(lodging_router, prefix="",
                   tags=["Lodgings"])


app.include_router(auth_router)

Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Workforce Lodging API"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


class OAuth2PasswordBearerWithCookie(OAuth2PasswordBearer):
    def __init__(self, tokenUrl: str):
        super().__init__(tokenUrl=tokenUrl)


oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="auth/login")
