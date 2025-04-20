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
uvicorn app.main:app --reload
```

### 1. Autenticación con JWT (JSON Web Token)
#### 1.1 /login Endpoint
Ejecutar con las credenciales de usuario `username`=`ivan` y `password`=`ivanpassword`. Devolverá un token JWT y otro CSRF.
```bash
curl -X POST "http://localhost:8000/login" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "username=ivan&password=ivanpassword"
```

#### 1.2 /protegido Endpoint
Ejecutar reemplazando `<jwt-token>` por el token devuelto por el servidor para acceder a endpoints protegidos mediante verificación JWT según esquema Bearer.
```bash
curl -X POST "http://localhost:8000/protegido" \
-H "Authorization: Bearer <jwt-token>"
```
### 2. Protección contra CSRF (Cross-Site Request Forgery) 
#### 2.1 /protegido Endpoint
```bash
curl -X <POST/PUT/DELETE> "http://localhost:8000/<endpoint>" \
-H "Authorization: Bearer <jwt-token>" \
-H "X-CSRF-Token: <csrf-token>"
```
