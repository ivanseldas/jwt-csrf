# JWT & CSRF Token

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
# Estructura de carpetas
```bash
.
├── app/
│   ├── main.py
│   ├── security.py      # lógica JWT & CSRF
│   ├── auth_router.py   # endpoints
│   ├── schemas.py       # modelos pydantic para validación de datos
│   └── database.py      # base de datos de usuarios
├── .env.example         # variables de entorno para claves y tiempos de expiración
├── requirements.txt
└── README.md
```
---
# Flujo de autenticación
1. **Login**  
   - El cliente envía credenciales `username` & `password` 
   - Si son válidas:  
     - **Genera JWT**: token firmado con datos del usuario `id`, `email` y tiempo de expiración
     - **Genera CSRF Token** 
     - **Almacenamiento**: guarda el CSRF token en el servidor asociado al usuario 
     - **Respuesta**: devuelve ambos tokens al cliente `JWT` & `CSRF`

2. **Acceso a recursos protegidos**  
   - **Para todos los ndpoints**:  
     - El cliente envía un JWT en el header `Authorization: Bearer <token>`.  
   - **Para métodos POST/PUT/DELETE**:  
     - El cliente añade header `X-CSRF-Token` con el CSRF recibido.  

3. **Validaciones**  
   - **JWT**:  
     1. Verifica la firma secreta con `SECRET_KEY`
     2. Verifica la fecha expiración 
     3. Obtiene los datos del usuario `id`, `email`  
   - **CSRF** (solo en métodos POST/PUT/DELETE):  
     1. Compara el token recibido con el almacenado
     2. Verifica la fecha expiración
     3. Usa `secrets.compare_digest()` para prevenir timing attacks
4. **CSRF en GET**: no se requiere (solo lectura). GET `/profile` solo necesita validar el JWT.
---
# Instalación y configuración
```bash
git clone https://github.com/ivanseldas/MTP-prueba-tecnica.git
cd MTP-prueba-tecnica
pip install -r requirements.txt
```
Crear un archivo `.env` basado en `.env.example`:
```bash
cp .env.example .env
```
---
# Ejecutar servidor
```bash
cd app
uvicorn main:app --reload
```
---
# Endpoints
### `/login` (autenticación con JWT token y CSRF token)
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

### `/protegido` (verificación de JWT Token y CSRF Token)
Ejecutar reemplazando `<jwt-token>` por el token devuelto `access_token` asi como `<csrf-token>` por `csrf_token` para validar ambos tokens.
```bash
curl -X <POST/PUT/DELETE> "http://localhost:8000/<endpoint>" \
-H "Authorization: Bearer <jwt-token>" \
-H "X-CSRF-Token: <csrf-token>"
```

### `/profile` (acceso a recurso protegido)
Ejecutar reemplazando `<jwt-token>` por el token devuelto `access_token`. En este caso no será necesario validar `csrf_token` ya que la acción realizada es `GET`.
```bash
curl -X GET "http://localhost:8000/profile" \
-H "Authorization: Bearer <jwt-token>" 
```
Devolverá la información básica del usuario una vez validado el JWT Token. Ejemplo de respuesta:
```bash
{"id":1,"username":"ivan","email":"ivan@gmail.com"}
```
