from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    gemini_api_key: str
    llm_model: str = "gemini-3.5-flash"
    embedding_model: str = "gemini-embedding-2"
    qdrant_url: str = "http://localhost:6333"
    
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()