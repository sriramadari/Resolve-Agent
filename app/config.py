from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    gemini_api_key: str
    llm_model: str = "gemini-3.5-flash"
    embedding_model: str = "gemini-embedding-2"
    qdrant_url: str = "http://localhost:6333"
    docs_collection: str = "razorpay_docs"
    top_k: int = 5
    score_threshold: float = 0.5
    
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()