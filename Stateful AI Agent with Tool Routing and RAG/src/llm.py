"""Azure OpenAI model factory."""

from __future__ import annotations

from langchain_openai import AzureChatOpenAI

from src.config import Settings, get_settings


def get_chat_model(settings: Settings | None = None) -> AzureChatOpenAI:
    """Create a deterministic Azure chat model that supports ``bind_tools``."""

    settings = settings or get_settings()
    settings.validate_azure()
    assert settings.azure_openai_api_key is not None
    assert settings.azure_openai_endpoint is not None
    assert settings.azure_openai_chat_deployment is not None

    return AzureChatOpenAI(
        api_key=settings.azure_openai_api_key.get_secret_value(),
        azure_endpoint=settings.azure_openai_endpoint,
        azure_deployment=settings.azure_openai_chat_deployment,
        api_version=settings.azure_openai_api_version,
        temperature=0,
        max_retries=2,
        timeout=60,
    )

