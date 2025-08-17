from model.utils.db_manager import ChatDbManager
from datetime import datetime

# Save message
def save_message(role, content, chat_db):
    with chat_db.conn:
        chat_db.conn.execute(
            "INSERT INTO messages (role, content) VALUES (?, ?)",
            (role, content)
        )


# Fetch last n messages
def get_last_n_messages(chat_db, n=5):
    cursor = chat_db.conn.cursor()
    cursor.execute(
        "SELECT role, content FROM messages ORDER BY timestamp DESC LIMIT ?",
        (n,)
    )
    return cursor.fetchall()[::-1]  # reverse to chronological order


def get_all_messages_log(chat_db: ChatDbManager):
    if chat_db.conn is None:
        raise RuntimeError("Chat DB connection is not established. Please call connect() first.")
    
    cursor = chat_db.conn.cursor()
    cursor.execute("SELECT * FROM messages ORDER BY timestamp DESC")
    return cursor.fetchall()
