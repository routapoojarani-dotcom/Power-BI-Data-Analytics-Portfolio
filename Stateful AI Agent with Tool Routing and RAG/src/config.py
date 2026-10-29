"""Environment configuration with beginner-friendly validation messages."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")


class Settings(BaseSettings):
    """Validated settings read from environment variables or a local `.env`."""

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    azure_openai_api_key: SecretStr | None = Field(default=None)
    azure_openai_endpoint: str | None = None
    azure_openai_api_version: str = "2024-10-21"
    azure_openai_chat_deployment: str | None = None

    max_agent_iterations: int = Field(default=10, ge=1, le=50)
    max_tool_calls: int = Field(default=20, ge=1, le=100)
    debug_agent: bool = False
    checkpoint_db_path: str | None = None

    flask_host: str = "127.0.0.1"
    flask_port: int = Field(default=5000, ge=1, le=65535)
    flask_debug: bool = True
    flask_secret_key: SecretStr | None = None
    max_user_message_length: int = Field(default=4000, ge=1, le=20000)

    use_faiss_rag: bool = False
    embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    rag_top_k: int = Field(default=5, ge=1, le=20)

    def validate_azure(self) -> None:
        """Raise one actionable error instead of a confusing SDK exception."""

        required = {
            "AZURE_OPENAI_API_KEY": self.azure_openai_api_key,
            "AZURE_OPENAI_ENDPOINT": self.azure_openai_endpoint,
            "AZURE_OPENAI_CHAT_DEPLOYMENT": self.azure_openai_chat_deployment,
        }
        missing = [name for name, value in required.items() if not value]
        if missing:
            joined = ", ".join(missing)
            raise ValueError(
                f"Azure OpenAI configuration is incomplete. Missing: {joined}. "
                "Copy .env.example to .env and add your Azure OpenAI values."
            )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return one settings object for the current process."""

    return Settings()


def reset_settings_cache() -> None:
    """Test helper for re-reading environment variables."""

    get_settings.cache_clear()

