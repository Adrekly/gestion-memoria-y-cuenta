FROM node:20-alpine

WORKDIR /app

# Copiar package files e instalar dependencias
COPY package.json package-lock.json* ./
RUN npm install

# Copiar código fuente
COPY . .

EXPOSE 5173

# Dev server con host 0.0.0.0 para acceso desde fuera del contenedor
CMD ["npx", "vite", "--host", "0.0.0.0", "--port", "5173"]