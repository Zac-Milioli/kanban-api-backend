"Arquivo de configuração de dados de ambiente"

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    "Classe para configuração de dados de ambiente"
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    DATABASE_URL: str
