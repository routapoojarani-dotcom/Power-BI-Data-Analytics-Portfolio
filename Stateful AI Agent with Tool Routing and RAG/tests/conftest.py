from __future__ import annotations

import pytest

from src.config import Settings


@pytest.fixture
def tutorial_settings() -> Settings:
    return Settings(
        max_agent_iterations=5,
        max_tool_calls=10,
        debug_agent=False,
        flask_debug=False,
        flask_secret_key="test-only-secret",
        _env_file=None,
    )

