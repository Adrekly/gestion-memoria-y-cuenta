"""
Configuración centralizada del sistema.
Usa Pydantic Settings para cargar variables de entorno.
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Configuración de la aplicación cargada desde variables de entorno."""

    # --- Aplicación ---
    APP_NAME: str = "Sistema de Gestión de Memoria y Cuenta - UNEG"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # --- MongoDB ---
    MONGO_URL: str = "mongodb://localhost:27017"
    MONGO_DB_NAME: str = "uneg_bienes"

    # --- Ollama (IA) ---
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "gemma:7b"

    # --- CORS ---
    CORS_ORIGINS: list[str] = ["*"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Retorna la instancia de configuración (cached)."""
    return Settings()
