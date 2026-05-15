from pydantic import BaseModel
from typing import List, Optional

class QueryRequest(BaseModel):
    session_id: str
    query: str

class QueryResponse(BaseModel):
    reply: str
    source_documents: List[str]
    domain: str

class ChatHistory(BaseModel):
    session_id: str
    role: str
    content: str
    timestamp: float
