from pydantic import BaseModel, EmailStr


class OAuth2RequestBody(BaseModel):
    grant_type: str | None = None
    username: EmailStr | None = None
    password: str | None = None
    refresh_token: str | None = None
    client_id: str | None = None
    client_secret: str | None = None
    redirect_uri: str | None = None


class Token(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "bearer"
