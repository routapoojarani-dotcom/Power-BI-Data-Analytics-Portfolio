"""Flask adapter for the shared LangGraph agent service."""

from __future__ import annotations

import logging
import secrets
from collections.abc import Callable
from typing import Any
from uuid import uuid4

from flask import Flask, jsonify, redirect, render_template, request, session, url_for

from src.agent_service import run_agent
from src.config import Settings, get_settings
from src.guardrails import InputValidationError
from src.utils import configure_logging

AgentRunner = Callable[[str, str | None], dict[str, Any]]
LOGGER = logging.getLogger(__name__)


def create_app(
    settings: Settings | None = None,
    agent_runner: AgentRunner | None = None,
) -> Flask:
    settings = settings or get_settings()
    configure_logging(settings.debug_agent)
    application = Flask(__name__)
    secret_key = (
        settings.flask_secret_key.get_secret_value()
        if settings.flask_secret_key
        else secrets.token_hex(32)
    )
    if not settings.flask_secret_key:
        LOGGER.warning("FLASK_SECRET_KEY is not set; using a temporary development key.")
    application.config.update(
        SECRET_KEY=secret_key,
        MAX_CONTENT_LENGTH=64 * 1024,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        AGENT_RUNNER=agent_runner or run_agent,
    )

    @application.get("/")
    def index() -> str:
        return render_template(
            "index.html",
            conversation=session.get("conversation", []),
            thread_id=session.get("thread_id"),
            last_activity=session.pop("last_activity", []),
            error=session.pop("error", None),
        )

    @application.post("/chat")
    def chat() -> Any:
        message = request.form.get("message", "")
        thread_id = session.get("thread_id") or str(uuid4())
        try:
            result = application.config["AGENT_RUNNER"](message, thread_id)
        except (InputValidationError, ValueError) as exc:
            session["error"] = str(exc)
            return redirect(url_for("index"))
        except Exception:
            LOGGER.exception("Agent request failed")
            session["error"] = "The agent could not complete the request. Check the server logs."
            return redirect(url_for("index"))

        conversation = list(session.get("conversation", []))
        conversation.extend(
            [
                {"role": "user", "content": message.strip()},
                {"role": "assistant", "content": result["answer"]},
            ]
        )
        session["conversation"] = conversation[-40:]
        session["thread_id"] = result["thread_id"]
        session["last_activity"] = result.get("steps", [])
        return redirect(url_for("index"))

    @application.post("/api/chat")
    def api_chat() -> Any:
        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            return jsonify({"error": "Request body must be a JSON object."}), 400
        try:
            result = application.config["AGENT_RUNNER"](
                payload.get("message", ""), payload.get("thread_id")
            )
        except (InputValidationError, ValueError) as exc:
            return jsonify({"error": str(exc)}), 400
        except Exception:
            LOGGER.exception("API agent request failed")
            return jsonify({"error": "The agent could not complete the request."}), 500
        return jsonify(result)

    @application.post("/new-chat")
    def new_chat() -> Any:
        session.pop("thread_id", None)
        session.pop("conversation", None)
        session.pop("last_activity", None)
        return redirect(url_for("index"))

    @application.errorhandler(404)
    def not_found(_error: Exception) -> tuple[str, int]:
        return render_template("error.html", message="Page not found."), 404

    @application.errorhandler(413)
    def too_large(_error: Exception) -> tuple[str, int]:
        return render_template("error.html", message="Request body is too large."), 413

    return application


app = create_app()

if __name__ == "__main__":
    current_settings = get_settings()
    app.run(
        host=current_settings.flask_host,
        port=current_settings.flask_port,
        debug=current_settings.flask_debug,
    )

