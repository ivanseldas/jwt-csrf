from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from security import (
    create_access_token, get_current_user, verify_password, ACCESS_TOKEN_EXPIRE_MINUTES,
    generate_csrf_token, store_csrf_token, validate_csrf
    )
from schemas import Token, User
from database import get_user
from datetime import timedelta

router = APIRouter()

# 1. Autenticación con JWT y CSRF tokens
@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Genera JWT token
    access_token = create_access_token(
        data={"sub": user["username"], "id": user["id"], "email": user["email"]},
        expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    # Genera CSRF Token
    csrf_token = generate_csrf_token()
    
    # Almacena CSRF Token
    store_csrf_token(user["username"], csrf_token)
    
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "csrf_token": csrf_token
        }

# 2. Validación de protección contra CSRF
@router.post("/protegido", dependencies=[Depends(validate_csrf)])
async def protected_post(user: User = Depends(get_current_user)):
    return {"message": "Acción POST exitosa: CSRF Token verificado", "user": user.username}

@router.put("/actualizar", dependencies=[Depends(validate_csrf)])
async def protected_put(user: User = Depends(get_current_user)):
    return {"message": "Recurso actualizado: CSRF Token verificado"}

@router.delete("/eliminar", dependencies=[Depends(validate_csrf)])
async def protected_delete(user: User = Depends(get_current_user)):
    return {"message": "Recurso eliminado: CSRF Token verificado"}


# 3. Endpoint accesible para usuarios autenticados (validación JWT)
@router.get("/profile", 
          response_model= User,
          summary="Obtener perfil de usuario",
          description="""Endpoint protegido que devuelve información del usuario autenticado.
                      Requiere validación JWT pero no CSRF token por ser método GET seguro.""")
async def get_user_profile(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email
    }