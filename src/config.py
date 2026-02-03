import os
from functools import lru_cache
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    groq_api_key: str
    tavily_api_key: str
    google_api_key: str
    
    # Model Config
    model_name: str = "openai/gpt-oss-120b"
    temperature: float = 0.7

    class Config:
        env_file = ".env"
        extra = "ignore"

@lru_cache
def get_settings():
    return Settings()

def get_llm():
    from langchain_groq import ChatGroq
    settings = get_settings()
    return ChatGroq(
        model=settings.model_name,
        temperature=settings.temperature,
        api_key=settings.groq_api_key
    )
