# 🏢 Sistema Integrado de Gestión de Bienes y Chatbot - UNEG

![Status](https://img.shields.io/badge/Status-En_Desarrollo-blue)
![Stack](https://img.shields.io/badge/Stack-React_|_FastAPI_|_MongoDB-success)
![IA](https://img.shields.io/badge/Model-Gemma:7b-orange)
![Docker](https://img.shields.io/badge/Deployment-Docker-blue?logo=docker)

Plataforma integral diseñada para la gestión, control y automatización del inventario de bienes nacionales de la **Universidad Nacional Experimental de Guayana (UNEG)**. Incluye un asistente virtual impulsado por inteligencia artificial local que interactúa con la base de datos para responder consultas de forma natural, garantizando la soberanía tecnológica y privacidad de los datos institucionales.

---

## ✨ Características Principales

* **📦 Control de Inventario:** Registro completo de bienes, movimientos (traslados, asignaciones) y procesos legales de desincorporación.
* **🔒 Privacidad Total (IA Local):** Ejecución del modelo **Gemma:7b** de forma local mediante **Ollama**, sin salida de datos a la nube.
* **⚡ Arquitectura Moderna:** Frontend reactivo construido con **React + Vite**, y una API backend robusta y tipada usando **FastAPI** y **Pydantic**.
* **🗄️ Base de Datos NoSQL:** Esquema flexible y persistente utilizando **MongoDB**.
* **🐳 Portabilidad:** Entorno completamente contenedorizado para un despliegue sin fricciones en cualquier sistema operativo usando **Docker Compose**.

---

## 🛠️ Requisitos del Sistema

Para asegurar un rendimiento fluido del ecosistema completo (especialmente del modelo de lenguaje de 7 billones de parámetros), se recomienda:

* **Memoria RAM:** 8GB (Mínimo) | 16GB (Recomendado).
* **Almacenamiento:** 10GB de espacio libre (para imágenes Docker, base de datos local y pesos del modelo de IA).
* **Software:** [Docker Desktop](https://www.docker.com/products/docker-desktop/) (o Docker Engine + Docker Compose) instalado y en ejecución.

---

## 🚀 Instalación y Despliegue

### 1. Clonar el Repositorio
```bash
git clone https://github.com/tu-usuario/gestion-memoria-y-cuenta.git
cd gestion-memoria-y-cuenta
```

### 2. Levantar la Infraestructura Completa
El proyecto incluye un archivo `docker-compose.yml` que orquesta la Base de Datos, el Backend, el Frontend y el motor de IA.
```bash
# Opcional: Detener contenedores previos y limpiar volúmenes
docker-compose down -v

# Levantar y construir todos los servicios en segundo plano
docker-compose up -d --build
```

### 3. Población de Datos Iniciales (Seeding)
Una vez que la infraestructura esté corriendo, carga el catálogo del clasificador SUDEBIP, sedes institucionales y datos de prueba:
```bash
docker cp "app/seeds/seed_all.js" uneg_mongodb:/tmp/seed_all.js
docker exec uneg_mongodb mongosh uneg_bienes --quiet /tmp/seed_all.js
```

### 4. Descarga del Modelo de IA (Ollama)
Si es la primera vez que ejecutas el proyecto, necesitas descargar el modelo de lenguaje en el contenedor de Ollama:
```bash
docker exec -it uneg_ollama ollama pull gemma:7b
```
*(Nota: Este paso puede tomar varios minutos dependiendo de tu conexión a internet).*

---

## 🌐 Servicios y Puertos

Una vez desplegado el stack, puedes acceder a los siguientes servicios en tu máquina local:

| Servicio | URL / Puerto | Descripción |
| :--- | :--- | :--- |
| **Frontend UI** | `http://localhost:5173` | Panel de control de inventario y Chatbot |
| **Backend API** | `http://localhost:8000` | Endpoints principales (FastAPI) |
| **API Docs (Swagger)**| `http://localhost:8000/docs` | Documentación interactiva para probar los endpoints |
| **MongoDB** | `mongodb://localhost:27018` | Acceso directo a la BD (Puerto **27018** en el host para evitar conflictos locales). Conectar vía *MongoDB Compass* a la base de datos `uneg_bienes`. |
| **Ollama** | `http://localhost:11434` | API del motor de IA local |

---

## 🏗️ Estructura del Proyecto
- `/app` - Core del Backend (FastAPI, Schemas Pydantic, Routers, Controladores de IA).
- `/frontend-uneg` - Código fuente del Frontend (React, Vite, CSS Vanilla para alto rendimiento).
- `/app/seeds` - Scripts de inicialización de datos para MongoDB.