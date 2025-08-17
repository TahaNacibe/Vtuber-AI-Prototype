import sqlite3

class ChatDbManager:
    def __init__(self, chat_db_path):
        self.conn = None
        self.chat_db_path = chat_db_path

    def connect(self):
        self.conn = sqlite3.connect(self.chat_db_path, check_same_thread=False)

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    def start_db(self):
        if self.conn is None:
            raise RuntimeError("Chat DB connection is not established. Please call connect() first.")

        with self.conn:
            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT,
                content TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """)

    def insert_message(self, role, content):
        with self.conn:
            self.conn.execute(
                "INSERT INTO messages (role, content) VALUES (?, ?)",
                (role, content)
            )

    def get_last_n_messages(self, n=10):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT role, content, timestamp FROM messages ORDER BY id DESC LIMIT ?",
            (n,)
        )
        return cursor.fetchall()
