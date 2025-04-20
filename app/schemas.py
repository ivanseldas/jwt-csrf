from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str
    csrf_token: str

class User(BaseModel):
    id: int
    username: str
    email: str