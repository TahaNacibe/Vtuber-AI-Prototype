import pytest
import sqlite3
from model.func.chat_db import save_message, get_last_n_messages, get_all_messages_log

class DummyChatDb:
    def __init__(self):
        self.conn = sqlite3.connect(":memory:")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT,
                content TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

@pytest.fixture
def chat_db():
    return DummyChatDb()

def test_save_and_get_last_n_messages(chat_db):
    save_message("user", "hello", chat_db)
    save_message("bot", "hi there", chat_db)
    messages = get_last_n_messages(chat_db, n=2)
    assert messages == [("user", "hello"), ("bot", "hi there")]

def test_get_all_messages_log(chat_db):
    save_message("user", "msg1", chat_db)
    save_message("bot", "msg2", chat_db)
    logs = get_all_messages_log(chat_db)
    assert len(logs) == 2
    assert logs[0][1] == "user" or logs[1][1] == "user"
