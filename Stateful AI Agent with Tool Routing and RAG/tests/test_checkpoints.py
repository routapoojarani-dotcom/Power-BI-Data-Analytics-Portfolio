
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver

from src.checkpoints import close_sqlite_connections, create_checkpointer
from src.config import Settings


def test_default_checkpointer_is_in_memory(tutorial_settings) -> None:
    assert isinstance(create_checkpointer(tutorial_settings), InMemorySaver)


def test_sqlite_checkpointer_is_created(tmp_path) -> None:
    settings = Settings(
        checkpoint_db_path=str(tmp_path / "checkpoints.sqlite3"),
        flask_secret_key="test",
        _env_file=None,
    )
    saver = create_checkpointer(settings)
    assert isinstance(saver, SqliteSaver)
    assert (tmp_path / "checkpoints.sqlite3").exists()
    close_sqlite_connections()

