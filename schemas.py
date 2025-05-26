from pydantic import BaseModel, EmailStr

class UsuarioCriar(BaseModel):
    email: EmailStr
    senha: str

class UsuarioLogin(BaseModel):
    email: EmailStr
    senha: str

class Token(BaseModel):
    acesso_token: str
    token_type: str