import time
from app.agents.graph import run_agent
from app.core.database import get_database

class ChatService:
    @staticmethod
    async def process_query(session_id: str, query: str):
        db = get_database()
        
        # Save user message
        timestamp = time.time()
        await db.execute(
            "INSERT INTO chat_history (session_id, role, content, timestamp) VALUES (?, ?, ?, ?)",
            (session_id, "user", query, timestamp)
        )
        await db.commit()
        
        # Run agent
        result = run_agent(query, session_id)
        
        # Save AI response
        ai_timestamp = time.time()
        await db.execute(
            "INSERT INTO chat_history (session_id, role, content, timestamp) VALUES (?, ?, ?, ?)",
            (session_id, "assistant", result["reply"], ai_timestamp)
        )
        await db.commit()
        
        return result
