# 🐾 PetCare API

API REST con **FastAPI + SQLite** para gestionar tus mascotas y sus pendientes.  
Incluye autenticación JWT, Swagger UI y CRUD completo.

---

## 🚀 Instalación rápida

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. (Opcional) Copiar y editar variables de entorno
cp .env.example .env

# 3. Arrancar el servidor
uvicorn main:app --reload
```

El servidor estará disponible en: **http://localhost:8000**

---

## 📚 Documentación interactiva

| UI | URL |
|---|---|
| **Swagger UI** | http://localhost:8000/docs |
| **ReDoc** | http://localhost:8000/redoc |

---

## 🔐 Autenticación

La API usa **JWT Bearer tokens**.

### Flujo:
1. `POST /auth/register` → crea cuenta, devuelve token
2. `POST /auth/login` → inicia sesión, devuelve token
3. En Swagger: clic en **Authorize** 🔒 → pega el token

### Endpoints de auth:
| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/auth/register` | Registrar nuevo usuario |
| POST | `/auth/login` | Iniciar sesión |
| GET | `/auth/me` | Ver mi perfil |
| PUT | `/auth/me` | Actualizar nombre/contraseña |

---

## 🐾 Mascotas — CRUD completo

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/pets/` | Crear mascota |
| GET | `/pets/` | Listar mis mascotas (filtro por especie) |
| GET | `/pets/{id}` | Ver detalle de mascota |
| PUT | `/pets/{id}` | Actualizar mascota |
| DELETE | `/pets/{id}` | Eliminar mascota (y sus pendientes) |

**Campos de mascota:** `name`, `species`, `breed`, `age_years`, `weight_kg`, `photo_url`, `notes`

---

## 📋 Pendientes por mascota — CRUD completo

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/pets/{id}/tasks/` | Crear pendiente |
| GET | `/pets/{id}/tasks/` | Listar pendientes (filtro por categoría/estado) |
| GET | `/pets/{id}/tasks/{task_id}` | Ver pendiente |
| PUT | `/pets/{id}/tasks/{task_id}` | Actualizar pendiente |
| PATCH | `/pets/{id}/tasks/{task_id}/toggle` | ✅ Marcar como hecho/pendiente |
| DELETE | `/pets/{id}/tasks/{task_id}` | Eliminar pendiente |

### Categorías disponibles:
`vacuna` · `veterinario` · `medicamento` · `baño` · `alimentacion` · `ejercicio` · `otro`

---

## 📁 Estructura del proyecto

```
petcare/
├── main.py              # Entry point, configuración FastAPI
├── requirements.txt
├── core/
│   ├── config.py        # Settings (SECRET_KEY, DB_URL, etc.)
│   ├── database.py      # SQLAlchemy engine y sesión
│   └── security.py      # JWT, hash de contraseñas, dependencias auth
├── models/
│   ├── user.py          # Modelo User
│   ├── pet.py           # Modelo Pet
│   └── task.py          # Modelo Task (pendientes)
├── schemas/
│   ├── user.py          # Pydantic schemas User
│   ├── pet.py           # Pydantic schemas Pet
│   └── task.py          # Pydantic schemas Task
└── routers/
    ├── auth.py          # Rutas de autenticación
    ├── pets.py          # CRUD mascotas
    └── tasks.py         # CRUD pendientes
```

---

## ⚙️ Variables de entorno (.env)

```env
SECRET_KEY=cambia-esto-en-produccion
DATABASE_URL=sqlite:///./petcare.db
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

---

## 🛠 Stack

- **FastAPI** — framework web
- **SQLAlchemy** — ORM
- **SQLite** — base de datos (cambiar a PostgreSQL en producción)
- **Pydantic** — validación de datos
- **python-jose** — JWT
- **passlib + bcrypt** — hash de contraseñas
