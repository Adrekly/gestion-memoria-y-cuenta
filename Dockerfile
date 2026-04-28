# Imagen ligera de Python
FROM python:3.11-slim

# Directorio de trabajo
WORKDIR /app

# Copiar e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Puerto de FastAPI
EXPOSE 8000

# Usar el nuevo entry point modular (app/main.py)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]