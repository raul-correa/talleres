from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # App
    ENV: str = "dev"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    PORT: int = 8000

    # Seguridad
    SECRET_KEY: str = "change-me"  # cámbialo en .env

    # Base de datos
    DATABASE_URL: str  # por defecto local

    model_config = SettingsConfigDict(
        env_file=".env",            # carga automáticamente .env en raíz del proyecto
        env_file_encoding="utf-8",
        extra="ignore",
    )

settings = Settings()