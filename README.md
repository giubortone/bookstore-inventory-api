# Bookstore Inventory API

API REST diseñada para la gestión de inventario de una cadena de librerías con cálculo de precios en tiempo real utilizando tasas de cambio externas.


## Tecnologías Utilizadas
Tecnología | Versión |
Python | 3.12 |
Django | 5.x |
Django REST Framework | - |
Docker & Docker Compose | - |
`requests` (para API externa) | - |


## Cómo Ejecutar el Proyecto
###  1. Ejecutar con Docker (Recomendado) 

1.  **Requisitos Previos:**
    * Tener instalado **Docker Desktop** y **Docker Compose**.

2.  **Pasos de ejecuciOn:**
docker compose up --build

**Detener contenedores**
docker compose down



### 2. Ejecutar sin Docker 
**Crear entorno virtual**
python -m venv venv

**Activar entorno virtual**
venv\Scripts\activate       # Windows
source venv/bin/activate    # Mac / Linux

**Instalar dependencias**
pip install -r requirements.txt

**Migrar BD**
python manage.py migrate

**Ejecutar servidor**
python manage.py runserver 0.0.0.0:8000


## Endpoints de la API

### Gestión de Libros (`/api/books/`)

| Método | Ruta | Descripción |
| `POST` | `/api/books/` | **Crear** un nuevo libro. |
| `GET` | `/api/books/` | **Listar** todos los libros (con paginación opcional). |
| `GET` | `/api/books/{id}` | **Obtener** los detalles de un libro por su `id`. |
| `PUT` | `/api/books/{id}` | **Actualizar** un libro completo por su `id`. |
| `PATCH` | `/api/books/{id}` | **Actualizar** un libro parcialmente por su `id`. |
| `DELETE` | `/api/books/{id}` | **Eliminar** un libro por su `id`. |
| `POST` | `/api/books/{id}/calculate-price/` | **Calcula** el precio de venta sugerido y 
| `GET` | `/api/books/search?category={category}` | **Busca** libros por la categoría 


## EJEMPLOS
**Crear un Libro  POST `/api/books/`** 
{
  "title": "El Quijote",
  "author": "Miguel de Cervantes",
  "isbn": "9788437604947",
  "cost_usd": 15.99,
  "stock_quantity": 25,
  "category": "Literatura Clásica",
  "supplier_country": "ES"
}

Response – 201 Created

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

**Listar Libros GET /api/books/**
Respuesta (200 OK):
[
  {
    "id": 1,
    "title": "El Quijote",
    "author": "Miguel de Cervantes",
    "cost_usd": 15.99,
    "selling_price_local": null
  }
]

**Buscar por Categoría GET /api/books/search?category=literatura**

Respuesta (200 OK):

[
  {
    "id": 1,
    "title": "El Quijote",
    "category": "Literatura Clásica"
  }
]

**Calcular Precio de Venta Sugerido POST /api/books/1/calculate-price**

Respuesta (200 OK):

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

## Colección de Postman:
Para probar fácilmente los endpoints, se incluye una colección de Postman lista para importar.
Ruta del archivo: /postman/bookstore-inventory-api.postman_collection.json

### ¿Cómo importarla?
1. Abrir **Postman**
2. Click en **Import**
3. Selecciona el archivo `.json` ubicado en la ruta


* **Link al repositorio (GitHub):** [https://github.com/giubortone bookstore-inventory-api]

AUTOR: GIULIANNA BORTONE 