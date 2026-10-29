from app import create_app


def fake_runner(message, thread_id=None):
    if not isinstance(message, str) or not message.strip():
        raise ValueError("Please enter a message before sending.")
    return {
        "answer": "Order ORD-1042 has shipped.",
        "thread_id": thread_id or "generated-thread",
        "tools_used": ["order_lookup"],
        "steps": [
            {"type": "received", "status": "success", "tool": None, "details": {}},
            {"type": "tool_call", "status": "success", "tool": "order_lookup", "details": {}},
            {"type": "tool_result", "status": "success", "tool": "order_lookup", "details": {}},
            {"type": "response", "status": "success", "tool": None, "details": {}},
        ],
        "iterations": 2,
        "errors": [],
    }


def test_home_page(tutorial_settings) -> None:
    client = create_app(tutorial_settings, fake_runner).test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert b"LangGraph AI Agent" in response.data


def test_html_chat_and_thread_session(tutorial_settings) -> None:
    client = create_app(tutorial_settings, fake_runner).test_client()
    response = client.post("/chat", data={"message": "Check order ORD-1042"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Order ORD-1042 has shipped" in response.data
    assert b"order_lookup" in response.data


def test_json_api(tutorial_settings) -> None:
    client = create_app(tutorial_settings, fake_runner).test_client()
    response = client.post(
        "/api/chat", json={"message": "Check order ORD-1042", "thread_id": "abc123"}
    )
    assert response.status_code == 200
    assert response.get_json()["thread_id"] == "abc123"
    assert response.get_json()["tools_used"] == ["order_lookup"]


def test_json_api_rejects_empty_and_non_json(tutorial_settings) -> None:
    client = create_app(tutorial_settings, fake_runner).test_client()
    assert client.post("/api/chat", json={"message": ""}).status_code == 400
    assert client.post("/api/chat", data="not-json").status_code == 400


def test_new_chat_clears_session(tutorial_settings) -> None:
    client = create_app(tutorial_settings, fake_runner).test_client()
    client.post("/chat", data={"message": "hello"})
    client.post("/new-chat")
    with client.session_transaction() as flask_session:
        assert "thread_id" not in flask_session
        assert "conversation" not in flask_session
