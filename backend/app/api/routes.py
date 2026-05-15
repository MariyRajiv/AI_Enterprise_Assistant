from fastapi import APIRouter
from app.models.schemas import QueryRequest, QueryResponse
from app.services.chat_service import ChatService

router = APIRouter()

@router.post("/query", response_model=QueryResponse)
async def query_assistant(request: QueryRequest):
    # Run the langgraph agent via ChatService
    result = await ChatService.process_query(request.session_id, request.query)
    return QueryResponse(
        reply=result["reply"],
        source_documents=[],
        domain=result["domain"]
    )
