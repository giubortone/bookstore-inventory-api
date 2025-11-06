# Bookstore Inventory API

API REST diseñada para la gestión de inventario de una cadena de librerías. El proyecto se centra en el **cálculo de precios de venta** integrándose con una API externa para obtener tasas de cambio.

---

## Tecnologías Utilizadas

| Tecnología               | Versión | Propósito                                      |
|--------------------------|---------|------------------------------------------------|
| **Python**               | 3.12    | Lenguaje de programación principal.           |
| **Django**               | 5.x     | Framework web principal.                      |
| **Django REST Framework**| -       | Construcción de los endpoints RESTful.        |
| **Docker & Docker Compose** | -    | Contenedorización para un entorno consistente.|
| **`requests`**           | -       | Cliente HTTP para la integración con la API de tasas de cambio. |

---

## Cómo Ejecutar el Proyecto

### 1. Ejecutar con Docker

1. **Requisitos Previos:**
   * Tener instalado **Docker Desktop** y **Docker Compose**.

2. **Pasos de Ejecución:**
   Ejecuta este comando en la raíz del proyecto para construir la imagen, iniciar el servicio y ejecutar las migraciones:

   ```bash
   docker compose up --build
   ```

   La API estará disponible en: [http://localhost:8000/api/books/](http://localhost:8000/api/books/)

3. **Detener Contenedores:**
   Ejecuta este comando para detener los contenedores en ejecución:
   ```bash
   docker compose down
1. **Crear entorno virtual:**
   ```bash
   python -m venv venv
   ```

2. **Activar entorno virtual (Windows):**
   ```bash
   venv\Scripts\activate
   ```

3. **Instalar Dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Migrar Base de Datos:**
   ```bash
   python manage.py migrate
   ```

5. **Ejecutar Servidor:**
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```
python manage.py migrate

5. **Ejecutar Servidor:**
python manage.py runserver 0.0.0.0:8000

## Endpoints de la API
### Gestión de Libros (`/api/books/`)
| Método | Ruta | Descripción |
| :--- | :--- | :--- |
| `POST` | `/api/books/` | **Crear** un nuevo libro. |
| `GET` | `/api/books/` | **Listar** todos los libros (con paginación opcional). |
| `GET` | `/api/books/{id}` | **Obtener** los detalles de un libro por su `id`. |
| `PUT` | `/api/books/{id}` | **Actualizar** un libro completamente por su `id`. |
| `PATCH` | `/api/books/{id}` | **Actualizar** un libro parcialmente (ej. solo el stock). |
| `DELETE` | `/api/books/{id}` | **Eliminar** un libro por su `id`. |

### Endpoints Especiales

| Método | Ruta | Descripción |
| :--- | :--- | :--- |
| `POST` | `/api/books/{id}/calculate-price/` | **Calcula** el precio de venta sugerido y actualiza `selling_price_local`. |
| `GET` | `/api/books/search?category={category}` | **Busca** libros por la categoría especificada. |

---


## Ejemplos de Uso de Endpoints

### 1. Crear un Libro (`POST /api/books/`)

**Request Body:**

```json
{
  "title": "El Quijote",
  "author": "Miguel de Cervantes",
  "isbn": "9788437604947",
  "cost_usd": 15.99,
  "stock_quantity": 25,
  "category": "Literatura Clásica",
  "supplier_country": "ES"
}
```

**Response – 201 Created:**

```json
{
  "id": 1,
  "title": "El Quijote",
  "author": "Miguel de Cervantes",
  "isbn": "9788437604947",
  "cost_usd": "15.99",
  "selling_price_local": null,
  "stock_quantity": 25,
  "category": "Literatura Clásica",
  "supplier_country": "ES",
  "created_at": "2025-11-06T16:55:32Z",
  "updated_at": "2025-11-06T16:55:32Z"
}
```

### 2. Calcular Precio de Venta Sugerido (`POST /api/books/{id}/calculate-price/`)

**Lógica Aplicada:** Toma `cost_usd`, obtiene la tasa de cambio, aplica el 40% de margen y actualiza el precio local.

**Response – 200 OK:**

```json
{
  "book_id": 1,
  "cost_usd": 15.99,
  "exchange_rate": 40,
  "cost_local": 639.6,
  "margin_percentage": 40,
  "selling_price_local": 895.44,
  "currency": "VES",
  "calculation_timestamp": "2025-01-15T10:30:00Z"
}
```

### 3. Buscar por Categoría (`GET /api/books/search?category=literatura`)

**Response – 200 OK:**

```json
[
  {
     "id": 1,
     "title": "El Quijote",
     "category": "Literatura Clásica"
  }
]
```

## Recursos

### Link al Repositorio (GitHub)
[https://github.com/giubortone/bookstore-inventory-api](https://github.com/giubortone/bookstore-inventory-api)

### Autor
**Giulianna Bortone**

### Colección de Postman
Para facilitar las pruebas de todos los endpoints, se incluye una colección de Postman.

**Ruta del archivo:** `/postman/bookstore-inventory-api.postman_collection.json`

#### Pasos para Importar:
1. Abrir Postman.
2. Hacer clic en **Import**.
3. Seleccionar el archivo `.json` ubicado en la ruta especificada.