# Usamos una imagen ligera de Node.js
FROM node:20-alpine

# Directorio de trabajo
WORKDIR /app

# Copiamos los archivos de dependencias
COPY package.json package-lock.json* ./

# Instalamos las dependencias
RUN npm install

# Copiamos el resto del código del frontend
COPY . .

# Exponemos el puerto de Vite
EXPOSE 5173

# Comando para iniciar el servidor de desarrollo exponiendo el host
CMD ["npm", "run", "dev", "--", "--host"]