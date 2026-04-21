# 🤖 Chatbot de Gestión de Activos - UNEG

![Status](https://img.shields.io/badge/Status-En_Desarrollo-blue)
![IA](https://img.shields.io/badge/Model-Gemma:7b-orange)
![Docker](https://img.shields.io/badge/Deployment-Docker-blue?logo=docker)

Asistente virtual inteligente diseñado para la consulta y gestión eficiente del inventario y activos de la **Universidad Nacional Experimental de Guayana (UNEG)**. Este sistema implementa IA local para garantizar la soberanía y privacidad de los datos institucionales.

---

## ✨ Características Principales

* **🔒 Privacidad Total:** Ejecución de modelo **Gemma:7b** de forma local mediante **Ollama**, sin salida de datos a la nube.
* **⚡ Arquitectura Moderna:** Frontend reactivo con **React + Tailwind CSS v4** y backend de alto rendimiento con **FastAPI**.
* **🧠 Orquestación de IA:** Uso de **LangChain** para la gestión de prompts y recuperación de información.
* **🐳 Portabilidad:** Entorno completamente contenedorizado con **Docker** y **Docker Compose**.

---

## 🛠️ Requisitos del Sistema

Para asegurar un rendimiento fluido del modelo de 7 billones de parámetros, se recomienda:

* **RAM:** 8GB (Mínimo) | 16GB (Recomendado).
* **Almacenamiento:** 10GB de espacio libre (para imágenes Docker y el modelo).
* **Software:** [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado y en ejecución.

---

## 🚀 Instalación y Despliegue

### 1. Clonar el Repositorio
```bash

git clone [https://github.com/tu-usuario/chatbot-activos-uneg.git](https://github.com/tu-usuario/chatbot-activos-uneg.git)
cd chatbot-activos-uneg

```

### 2. Levantar Infraestructura
```bash

gdocker-compose down -v
docker-compose up -d --build

```

### 3. Configuración del Modelo de IA
```bash

docker exec -it uneg_ollama ollama pull gemma:7b ### solo si tiene más de 8gb de ram

```

|       Servicio    |              URL              | Descripción                       |
| :---              |            :---               |         :---                      |
| **Frontend**      | `http://localhost:5173`       | Interfaz de usuario (Chat)        |
| **Backend API**   | `http://localhost:8000`       | Core del sistema (FastAPI)        |
| **Documentación** | `http://localhost:8000/docs`  | Swagger UI para pruebas de API    |

epale