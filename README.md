# 📝 To Do List API

API RESTful para la gestión de listas de tareas, desarrollada con **FastAPI** y arquitectura hexagonal.

---

## 📑 Tabla de Contenidos

- [Tecnologías utilizadas](#-tecnologías-utilizadas)
- [Estructura del proyecto](#-estructura-del-proyecto)
- [Configuración del entorno local](#-configuración-del-entorno-local)
- [Variables de entorno](#-variables-de-entorno)
- [Ejecución con Docker](#-ejecución-con-docker)
- [Ejemplos de uso de la API](#-ejemplos-de-uso-de-la-api)
- [Pruebas](#-ejecutar-pruebas)
- [Linter y formateo](#-linter-y-formateo)
- [Contribución](#-contribución)
- [Licencia](#-licencia)

---

## 🚀 Tecnologías utilizadas

- **Lenguaje**: Python 3.11
- **Framework**: FastAPI
- **Base de datos**: PostgreSQL (contenedorizada)
- **ORM**: SQLAlchemy
- **Validaciones**: Pydantic
- **Testing**: Pytest (≥75% cobertura)
- **Linter**: flake8
- **Formateo**: black
- **Contenerización**: Docker + Docker Compose

---

## 🧱 Estructura del proyecto

```text
todo_list_api/
├── app/
│   ├── domain/
│   ├── application/
│   ├── infrastructure/
│   ├── shared/
├── tests/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .flake8
├── pytest.ini
└── README.md
```

---

## 🧑‍💻 Configuración del entorno local

1. Clona el repositorio:
    ```bash
    git clone https://github.com/lgarciao/todo_list_api.git
    cd todo_list_api
    ```

2. Crea un entorno virtual (se deberá tener instalado python 3.11):
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Linux/macOS
    venv\Scripts\activate     # En Windows
    ```

3. Instala dependencias:
    ```bash
    pip install -r requirements.txt
    ```

---

## 🔑 Variables de entorno

Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/todo_db
```

---

## 🐳 Ejecución con Docker

1. Levanta los servicios:
    ```bash
    docker-compose up --build
    ```

2. Accede a la API en:
    - **URL base:** [http://localhost:8000](http://localhost:8000)

3. Documentación interactiva:
    - [Swagger UI](http://localhost:8000/docs)
    - [ReDoc](http://localhost:8000/redoc)

---

## 📦 Ejemplos de uso de la API

### Crear una lista

```http
POST /todo-lists/
Content-Type: application/json

{
  "name": "Mi lista",
  "description": "Tareas personales"
}
```

### Respuesta exitosa

```json
{
  "id": "uuid",
  "name": "Mi lista",
  "description": "Tareas personales",
  "created_at": "2025-08-07T12:00:00Z",
  "updated_at": "2025-08-07T12:00:00Z"
}
```

---

### Obtener todas las listas

```http
GET /todo-lists/
```

### Obtener una lista por ID

```http
GET /todo-lists/{list_id}
```

### Actualizar una lista

```http
PUT /todo-lists/{list_id}
Content-Type: application/json

{
    "name": "Lista actualizada",
    "description": "Descripción actualizada"
}
```

### Eliminar una lista

```http
DELETE /todo-lists/{list_id}
```

---

### Crear una tarea

```http
POST /todo-lists/{list_id}/tasks/
Content-Type: application/json

{
    "title": "Comprar leche",
    "description": "Ir al supermercado",
    "priority": "HIGH"
}
```

### Listar tareas de una lista

```http
GET /todo-lists/{list_id}/tasks/
```

### Cambiar el estado de una tarea

```http
PATCH /tasks/{task_id}/status
Content-Type: application/json

{
    "status": "COMPLETED"
}
```

### Obtener porcentaje de completitud de una lista

```http
GET /todo-lists/{list_id}/completion-percentage
```

---

## 🧪 Ejecutar pruebas

```bash
pytest --cov=app tests/
```
La cobertura mínima esperada es de **75%**.

---

## 🧹 Linter y formateo

- Ejecutar flake8:
    ```bash
    flake8 app/
    ```
- Formatear con black:
    ```bash
    black app/
    ```

---

## 🤝 Contribución

¡Las contribuciones son bienvenidas! Por favor, abre un issue o pull request para sugerencias o mejoras.

---

## 📄 Licencia

Este proyecto está bajo la licencia MIT.

---
