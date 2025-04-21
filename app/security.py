from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status, Depends, Request
from database import get_user
from schemas import User
from dotenv import load_dotenv
import os
import secrets

# Carga archivo .env
load_dotenv()

# Carga las variables de entorno del archivo .env
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
CSRF_TOKEN_EXPIRE_MINUTES = int(os.getenv("CSRF_TOKEN_EXPIRE_MINUTES"))


# 1. Configuración para validación mediante JWT

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Verifica que la contraseña como string y hasheada coinciden
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# Crea un jwt token con la fecha de expiración y la firma secreta
def create_access_token(data: dict, expires_time: timedelta):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_time
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Comprueba que el token enviado por el cliente es igual al token enviado desde el servidor
async def get_current_user(token: str = Depends(oauth2_scheme)):
    error_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid Token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decodifica el token para obtener el contenido del mismo
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # Obtiene el nombre de usuario del contendio del token decodificado
        username: str = payload.get("sub")
        # Devuelve el usuario si el usuario de cliente y servidor obtenidos del token jwt coinciden
        if username is None:
            raise error_exception
        user = get_user(username)
        if user is None:
            raise error_exception
        return User(**user)
    except JWTError:
        raise error_exception
 
    
# 2. Funciones para CSRF Token 

CSRF_TOKENS = {}

def generate_csrf_token() -> str:
    return secrets.token_urlsafe(32)

def store_csrf_token(username: str, token: str):
    expiration_time = datetime.now(timezone.utc) + timedelta(minutes=CSRF_TOKEN_EXPIRE_MINUTES)
    CSRF_TOKENS[username] = {
        "token": token,
        "expiration": expiration_time.timestamp()
    }

async def validate_csrf(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    if request.method in ["POST", "PUT", "DELETE"]:
        csrf_token = request.headers.get("X-CSRF-Token")
        
        if not csrf_token:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="CSRF token requerido"
            )
        
        # Obtiene token almacenado
        stored_token = CSRF_TOKENS[current_user.username]
        
        if not stored_token:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="CSRF token no generado"
            )
           
        # Verifica expiración de token
        current_time = datetime.now(timezone.utc).timestamp()
        if current_time > stored_token["expiration"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="CSRF token expirado"
            )
        
        if not secrets.compare_digest(csrf_token, stored_token['token']):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="CSRF token inválido"
            )