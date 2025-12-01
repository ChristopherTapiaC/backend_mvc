# Tienda MVC (Django + Tailwind)

Aplicación MVC simple para gestionar **Productos, Clientes y Ventas** con un flujo de **carrito** (agregar/quitar ítems y confirmar) y **edición de ventas** ya registradas. Incluye **dashboard** (Home) con KPIs y gráficos (Chart.js).

---

## 🧩 Requisitos

- **Python 3.10+** (probado con 3.12)
- **pip**
- (Opcional) **venv** para entorno virtual
- No se requiere Node ni compilación manual de CSS (usa Tailwind vía CDN)

---

## ⚙️ Instalación

```bash
# 1) Clonar el repositorio
git clone <URL_DEL_REPO>
cd <CARPETA_DEL_PROYECTO>

# 2) (Opcional) Crear entorno virtual
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

# 3) Instalar dependencias
# Si existe el archivo requirements.txt
pip install -r requirements.txt

# O instalación mínima
pip install "Django>=5,<6"
```

---

## 🚀 Cómo ejecutar

### 1️⃣ Crear base de datos
```bash
python manage.py migrate
```

### 2️⃣ (Opcional) Crear superusuario
```bash
python manage.py createsuperuser
```

### 3️⃣ Cargar datos iniciales

**Opción A – Fixture `seed.json` (si está incluido):**
```bash
python manage.py loaddata seed.json
```

**Opción B – Script inline (crea datos básicos):**
```bash
python manage.py shell <<'PY'
from store.catalog.models import Product, Client
if not Product.objects.exists():
    Product.objects.bulk_create([
        Product(name="Teclado", price=15000),
        Product(name="Telefono", price=250000),
        Product(name="Computador", price=500000),
        Product(name='Monitor 144Hz 32"', price=450000),
    ])
if not Client.objects.exists():
    Client.objects.bulk_create([
        Client(name="Christopher Tapia", email="chris@example.com", phone="+56911111111"),
        Client(name="Tihare Aguirre", email="tihare@example.com", phone="+56922222222"),
        Client(name="Pedro Picapedra", email="pedro@example.com", phone="+56933333333"),
    ])
print("Datos iniciales OK")
PY
```

### 4️⃣ Iniciar servidor
```bash
py manage.py runserver
```
- App: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

---

## 🧠 Descripción funcional

### 🛍️ Productos
- CRUD completo (Listar / Crear / Editar / Eliminar).
- Validación de precios (≥ 0).
- Diseño responsivo con scroll horizontal solo en móvil.

### 👥 Clientes
- CRUD completo con validación de correo y teléfono.

### 💸 Ventas
- Flujo completo:
  1. Selección de cliente.
  2. Agregar/quitar productos al carrito.
  3. Confirmación de venta (POST con CSRF).
- Ventas independientes por cliente.
- Edición posterior (agregar o eliminar ítems).
- Totales y subtotales calculados con `Decimal` para precisión.
- Edición por POST, sin riesgo de GET destructivos.

### 📊 Dashboard (Home)
- KPIs: Total vendido, cantidad de ítems, clientes con compras, número de ventas y productos.
- Gráficos con Chart.js: productos más vendidos y clientes con más compras.

---

## 🌐 Rutas principales

| Sección | Ruta | Descripción |
|----------|------|--------------|
| Home | `/` | Dashboard |
| Productos | `/products/` | CRUD de productos |
| Clientes | `/clients/` | CRUD de clientes |
| Ventas | `/sales/` | Listado y flujo de ventas |
| Editar venta | `/sales/<id>/edit/` | Modificar una venta existente |

---

## 🗂️ Estructura del proyecto

```
store/
  manage.py
  store/
    __init__.py
    settings.py
    urls.py
    wsgi.py
  catalog/
    models.py
    views.py
    urls.py
    forms.py
    templates/catalog/
      base.html
      home.html
      client_list.html
      client_form.html
      product_list.html
      product_form.html
      sale_list.html
      sale_start.html
      sale_cart.html
      sale_edit.html
  db.sqlite3 (opcional para evaluación)
requirements.txt
README.md
```

---

## 💾 Base de datos

- Usa **SQLite** por defecto (`db.sqlite3`).
- Si no está incluida, se genera con `python manage.py migrate`.
- Los datos de ejemplo pueden cargarse mediante `loaddata` o script inline.

### Tablas principales:
- **Product:** `name`, `price`, `create_in`
- **Client:** `name`, `email`, `phone`, `create_in`
- **Sale:** `client`, `created_at`, `total`
- **SaleDetail:** `sale`, `product`, `quantity`, `subtotal`

---

## 🧰 Comandos útiles

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Cargar fixture
python manage.py loaddata seed.json

# Ejecutar servidor
python manage.py runserver
```

---

## 📝 Notas adicionales

- La ruta raíz (`/`) carga la vista `home.html`.
- En edición de ventas, se usa `line_total` para evitar conflictos con propiedades del modelo.
- Acciones destructivas (eliminar ítem, venta o detalle) se hacen siempre por POST con CSRF.
- Diseño responsive basado en Tailwind con estilo uniforme en todas las vistas.

---

© 2025 - Desarrollado por **Christopher Tapia** | Proyecto Django MVC + TailwindCSS
