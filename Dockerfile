# Imagen base
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt /app/

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000

# Comando por defecto: ejecutar Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
