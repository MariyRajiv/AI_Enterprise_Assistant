import os
import aiosqlite

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "enterprise_assistant.db")

class Database:
    connection: aiosqlite.Connection = None

db = Database()

async def connect_to_db():
    db.connection = await aiosqlite.connect(DB_PATH)
    # Create the chat history table if it doesn't exist
    await db.connection.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp REAL NOT NULL
        )
    ''')
    await db.connection.commit()
    print("Connected to SQLite database")

async def close_db_connection():
    if db.connection is not None:
        await db.connection.close()
        print("Closed SQLite connection")

def get_database():
    return db.connection
