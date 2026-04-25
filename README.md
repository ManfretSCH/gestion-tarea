# 📝 Gestión de Tareas API

API REST para gestionar usuarios y sus tareas, construida con FastAPI y SQLAlchemy.

## 🚀 Tecnologías

- **Python** 3.12
- **FastAPI** — Framework web
- **SQLAlchemy** — ORM para base de datos
- **PyMySQL** — Conector MySQL
- **Pydantic** — Validación de datos
- **uv** — Gestor de dependencias
- **Uvicorn** — Servidor ASGI

## 📁 Estructura del proyecto

```
├── app/
│   ├── main.py        # Configuración principal de la app
│   ├── database.py    # Conexión a la base de datos
│   ├── models.py      # Modelos de SQLAlchemy (User, Task)
│   ├── schemas.py     # Esquemas de Pydantic
│   └── routers/
│       ├── users.py   # Endpoints de usuarios
│       └── tasks.py   # Endpoints de tareas
└── main.py            # Punto de entrada
```

## ⚙️ Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/ManfretSCH/gestion-tarea.git
cd gestion-tarea
```

2. Instalar dependencias con uv:
```bash
uv sync
```

3. Crear un archivo `.env` en la raíz del proyecto con la URL de tu base de datos:
```env
DATABASE_URL=mysql+pymysql://usuario:contraseña@localhost/nombre_db
```

4. Ejecutar el servidor:
```bash
fastapi dev main.py
```

La API estará disponible en `http://localhost:8000`.  
La documentación interactiva en `http://localhost:8000/docs`.

## 📌 Endpoints

### Usuarios — `/users`

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/users/` | Listar todos los usuarios |
| `GET` | `/users/{user_id}` | Obtener un usuario por ID |
| `POST` | `/users/` | Crear un nuevo usuario |
| `PATCH` | `/users/{user_id}` | Actualizar un usuario |
| `DELETE` | `/users/{user_id}` | Eliminar un usuario y sus tareas |

### Tareas — `/users/{user_id}/tasks`

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/users/{user_id}/tasks/` | Listar tareas de un usuario (filtro opcional por `completed`) |
| `GET` | `/users/{user_id}/tasks/{task_id}` | Obtener una tarea por ID |
| `POST` | `/users/{user_id}/tasks/` | Crear una nueva tarea |
| `PATCH` | `/users/{user_id}/tasks/{task_id}` | Actualizar una tarea |
| `DELETE` | `/users/{user_id}/tasks/{task_id}` | Eliminar una tarea |

## 🗄️ Modelos

### User
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | Integer | Identificador único |
| `name` | String | Nombre del usuario |
| `email` | String | Email único del usuario |
| `age` | Integer | Edad del usuario |

### Task
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | Integer | Identificador único |
| `title` | String | Título de la tarea |
| `description` | String | Descripción (opcional) |
| `completed` | Boolean | Estado de la tarea (default: `false`) |
| `user_id` | Integer | ID del usuario propietario |