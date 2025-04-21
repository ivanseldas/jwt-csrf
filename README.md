# MTP-prueba-tecnica

### 1. Autenticación con JWT (JSON Web Token)
- Endpoint `/login` valida credenciales y devuelve JWT  
- Token incluye: ID/user, email + expiración (15 min)  
- Validación automática en headers `Authorization: Bearer <token>`  

### 2. Protección contra CSRF (Cross-Site Request Forgery)  
- Token CSRF generado en login y enviado en header `X-CSRF-Token`  
- Validación obligatoria en métodos **POST/PUT/DELETE**  

### 3. Endpoint de Ejemplo `/profile`
- **GET** seguro con validación JWT (no requiere CSRF)
- Devuelve: ID, username y email del usuario  

---
### Instalación
```bash
git clone https://github.com/ivanseldas/MTP-prueba-tecnica.git
cd MTP-prueba-tecnica
pip install -r requirements.txt
```
### Configuración
Crear un archivo `.env` basado en `.env.example`:
```bash
cp .env.example .env
```

### Ejecutar servidor
```bash
cd app
uvicorn main:app --reload
```

### /login Endpoint (autenticación con JWT token y CSRF token)
Ejecutar con las credenciales de usuario `username`=`ivan` y `password`=`ivanpassword`. Devolverá un token JWT y otro CSRF.
```bash
curl -X POST "http://localhost:8000/login" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "username=ivan&password=ivanpassword"
```
Ejemplo de respuesta:
```bash
{"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJpdmFuIiwiaWQiOjEsImVtYWlsIjoiaXZhbkBnbWFpbC5jb20iLCJleHAiOjE3NDUxOTE0NDN9.qsYv9SLfvzi9inxHiA1YLJK7UOHxMUMzwy5p0TsAFEk", \
"token_type":"bearer", \
"csrf_token":"ppJHXNgLXhx2dzMYWZ1H5sUSx_L90o3XO54TkEKds_Y"}
```

### /protegido Endpoint (verificación de JWT Token y CSRF Token)
Ejecutar reemplazando `<jwt-token>` por el token devuelto `access_token` asi como `<csrf-token>` por `csrf_token` para validar ambos tokens.
```bash
curl -X <POST/PUT/DELETE> "http://localhost:8000/<endpoint>" \
-H "Authorization: Bearer <jwt-token>" \
-H "X-CSRF-Token: <csrf-token>"
```

### /profile Endpoint (acceso a recurso protegido)
Ejecutar reemplazando `<jwt-token>` por el token devuelto `access_token`. En este caso no será necesario validar `csrf_token` ya que la acción realizada es `GET`.
```bash
curl -X GET "http://localhost:8000/profile" \
-H "Authorization: Bearer <jwt-token>" 
```
Devolverá la información básica del usuario una vez validado el JWT Token. Ejemplo de respuesta:
```bash
{"id":1,"username":"ivan","email":"ivan@gmail.com"}
```
