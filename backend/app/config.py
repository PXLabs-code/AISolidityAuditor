from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    data_dir: Path = Path("./data/jobs")
    max_upload_mb: int = 10
    max_zip_files: int = 200
    max_zip_file_mb: int = 2
    max_extracted_mb: int = 30
    slither_timeout_sec: int = 120
    max_ai_findings: int = 20
    job_retention_hours: int = 24
    ai_provider: str = "openai"
    openai_api_key: str = ""
    openai_base_url: str = "https://api.openai.com/v1"
    openai_model: str = "gpt-4o-mini"
    anthropic_api_key: str = ""
    claude_model: str = "claude-3-5-haiku-latest"
    deepseek_api_key: str = ""
    deepseek_base_url: str = "https://api.deepseek.com/v1"
    deepseek_model: str = "deepseek-chat"
    cors_origins: str = "http://localhost:5173,http://localhost:3000"


settings = Settings()
