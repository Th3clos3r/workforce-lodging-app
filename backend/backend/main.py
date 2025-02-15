from fastapi import FastAPI
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel, OAuthFlowPassword
from fastapi.security import OAuth2
from backend.auth_routes import router as auth_router
from backend.database import engine, Base


app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Workforce Lodging API"}


class OAuth2PasswordBearerWithCookie(OAuth2):
    def __init__(self, tokenUrl: str):
        flows = OAuthFlowsModel(password=OAuthFlowPassword(tokenUrl=tokenUrl))
        super().__init__(flows=flows)


oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="auth/login")


app.include_router(auth_router, prefix="/auth")
