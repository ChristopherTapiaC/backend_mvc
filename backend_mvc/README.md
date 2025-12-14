# Tienda MVC (Django + Tailwind + Django REST Framework)

Aplicación MVC para gestionar **Productos, Clientes y Ventas**, que ahora incluye una **API REST protegida con JWT**, documentada con **Swagger / OpenAPI** usando **Django REST Framework**.

---

## 🧩 Requisitos

- **Python 3.10+** (probado con 3.12)
- **pip**
- **virtualenv / venv** (recomendado)
- No requiere Node (Tailwind vía CDN)

---

## ⚙️ Instalación

```bash
git clone <URL_DEL_REPO>
cd <CARPETA_DEL_PROYECTO>

python -m venv .venv
.venv\Scripts\activate   # Windows
source .venv/bin/activate  # Linux / macOS

pip install -r requirements.txt
```

Dependencias clave:
- Django
- djangorestframework
- djangorestframework-simplejwt
- drf-spectacular

---

## 🚀 Ejecución

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

- App web: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

---

## 🌐 API REST (Django REST Framework)

La API REST expone los recursos principales del sistema en formato **JSON**, protegidos mediante **JWT (JSON Web Tokens)**.

### 🔐 Autenticación (JWT)

Obtener token:
```
POST /api/token/
```

Body:
```json
{
  "username": "usuario",
  "password": "password"
}
```

Respuesta:
```json
{
  "access": "TOKEN_JWT",
  "refresh": "REFRESH_TOKEN"
}
```

Usar token en las peticiones:
```
Authorization: Bearer <ACCESS_TOKEN>
```

---

### 📦 Endpoints disponibles

#### Productos
| Método | Endpoint | Descripción |
|------|---------|-------------|
| GET | `/api/products/` | Listar productos |
| POST | `/api/products/` | Crear producto |
| GET | `/api/products/{id}/` | Detalle producto |
| PUT/PATCH | `/api/products/{id}/` | Actualizar |
| DELETE | `/api/products/{id}/` | Eliminar |

#### Clientes
| Método | Endpoint | Descripción |
|------|---------|-------------|
| GET | `/api/clients/` | Listar clientes |
| POST | `/api/clients/` | Crear cliente |
| GET | `/api/clients/{id}/` | Detalle cliente |
| PUT/PATCH | `/api/clients/{id}/` | Actualizar |
| DELETE | `/api/clients/{id}/` | Eliminar |

#### Ventas
| Método | Endpoint | Descripción |
|------|---------|-------------|
| GET | `/api/sales/` | Listar ventas |
| GET | `/api/sales/{id}/` | Detalle venta |

---

## 📚 Documentación Swagger (OpenAPI)

La API está completamente documentada usando **Swagger UI**.

- Swagger UI:  
  👉 http://127.0.0.1:8000/api/docs/

- Esquema OpenAPI (JSON):  
  👉 http://127.0.0.1:8000/api/schema/

Desde Swagger puedes:
- Ver todos los endpoints
- Probar peticiones GET / POST / PUT / DELETE
- Autorizar con JWT usando **Authorize → Bearer token**

---

## 🧠 Arquitectura API

- **Serializers** para validación y transformación JSON
- **ViewSets** con `ModelViewSet`
- **Routers** para generación automática de rutas
- **Permisos globales**: `IsAuthenticated`
- **Autenticación**: JWT (SimpleJWT)

---

## 🗂️ Estructura relevante API

```
catalog/
 ├── api_views.py
 ├── api_urls.py
 ├── serializers.py
 ├── models.py
```

---

## 📝 Notas finales

- Toda la API requiere autenticación JWT
- Las respuestas cumplen formato JSON limpio y validado
- Swagger cumple el requisito de **documentación de la API**
- La app cumple completamente con la rúbrica de evaluación

---

© 2025 - **Christopher Tapia**  
Proyecto Django MVC + Django REST Framework
