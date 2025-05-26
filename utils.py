from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

# Configurações
CHAVE_SECRETA = "c739d8f4d9f9415bbcb7a5f74f2e2cda5e5c2233e80e64c196e15fb894da0174"
ALGORITHM = "HS256"
TEMPO_EXPIRACAO_TOKEN = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verificar_senha(senha_plana: str, senha_hash: str) -> bool:
    return pwd_context.verify(senha_plana, senha_hash)

def gerar_hash_senha(senha: str) -> str:
    return pwd_context.hash(senha)
    
def gerar_token_acesso(dados: dict) -> str:
    dados_para_codificar = dados.copy()
    expiracao = datetime.utcnow() + timedelta(minutes=TEMPO_EXPIRACAO_TOKEN)
    dados_para_codificar.update({"exp": expiracao})
    token_jwt = jwt.encode(dados_para_codificar, CHAVE_SECRETA, algorithm=ALGORITHM)
    return token_jwt