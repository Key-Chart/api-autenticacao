from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated

from models import Usuario
from schemas import UsuarioCriar, UsuarioLogin, Token
from utils import (
    verificar_senha,
    gerar_hash_senha,
    gerar_token_acesso
)
from database import SessionLocal, Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/cadastro", response_model=Token)
async def cadastrar_usuario(usuario: UsuarioCriar, db: Session = Depends(get_db)):
    usuario_existente = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado"
        )
    senha_hash = gerar_hash_senha(usuario.senha)
    novo_usuario = Usuario(email=usuario.email, senha_hash=senha_hash)
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    token_acesso = gerar_token_acesso(
        dados={"sub": usuario.email, "id": novo_usuario.id}
    )

    return {"acesso_token": token_acesso, "token_type": "bearer"}

@app.post("/login", response_model=Token)
async def fazer_login(usuario: UsuarioLogin, db: Session = Depends(get_db)):
    usuario_db = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if not usuario_db or not verificar_senha(usuario.senha, usuario_db.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token_acesso = gerar_token_acesso(
        dados={"sub": usuario.email, "id": usuario_db.id}
    )
    return {"acesso_token": token_acesso, "token_type": "bearer"}
