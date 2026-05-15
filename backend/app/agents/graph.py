from typing import TypedDict, Sequence, Annotated
from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_ollama import ChatOllama
import operator
import json
from app.rag.vector_store import get_retriever

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    query: str
    domain: str
    context: str

# Define the Ollama LLM using the modern langchain-ollama package
llm = ChatOllama(model="mistral", temperature=0)

def classify_query(state: AgentState):
    query = state["query"]
    q_lower = query.lower().strip()
    
    # Fast path for basic greetings to avoid slow LLM call
    greetings = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening", "hi there", "hello there"]
    if q_lower in greetings or (len(q_lower.split()) <= 3 and any(g in q_lower for g in greetings)):
        return {"domain": "custom"}

    prompt = f"""
    You are an intelligent router. Classify the user query into exactly one of these three categories:
    - 'university': If the query is about admissions, placements, faculty, syllabus, or university info.
    - 'company': If the query is about Infosys, HR policies, or company overview.
    - 'custom': If the query is a general greeting, fallback, or something else.
    
    Return ONLY a JSON object with a single key 'domain' and the value being the category.
    Query: {query}
    """
    response = llm.invoke([HumanMessage(content=prompt)])
    try:
        content = response.content.strip()
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].strip()
            
        parsed = json.loads(content)
        domain = parsed.get("domain", "custom")
        if domain not in ["university", "company", "custom"]:
            domain = "custom"
    except Exception as e:
        print(f"Classification error: {e}")
        domain = "custom"
        
    return {"domain": domain}

def retrieve_context(state: AgentState):
    domain = state["domain"]
    query = state["query"]
    
    if domain == "custom":
        return {"context": "GENERAL_CONVERSATION: No specific documents needed."}
    
    try:
        retriever = get_retriever(domain)
        docs = retriever.invoke(query)
        context = "\n\n".join([doc.page_content for doc in docs])
        return {"context": context}
    except Exception as e:
        print(f"Retrieval error: {e}")
        return {"context": ""}

def generate_response(state: AgentState):
    query = state["query"]
    context = state["context"]
    domain = state["domain"]
    
    if "GENERAL_CONVERSATION" in context:
        system_prompt = "You are a helpful AI Enterprise Assistant. Engage in friendly conversation, but be VERY concise. Keep your responses short (1-2 sentences maximum)."
    else:
        system_prompt = f"""
        You are an AI Enterprise Assistant. Use the provided context to answer the user's query about {domain} in detail.
        Extract and synthesize the relevant information from the context. If the context contains partial information, provide what you know.
        If the context is completely unrelated or missing, say "I don't have enough internal context to answer this."
        
        Context:
        {context}
        """
    
    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=query)
    ])
    return {"messages": [AIMessage(content=response.content)]}

# Build LangGraph Workflow
workflow = StateGraph(AgentState)
workflow.add_node("classify", classify_query)
workflow.add_node("retrieve", retrieve_context)
workflow.add_node("generate", generate_response)

workflow.set_entry_point("classify")
workflow.add_edge("classify", "retrieve")
workflow.add_edge("retrieve", "generate")
workflow.add_edge("generate", END)

agent_app = workflow.compile()

def run_agent(query: str, session_id: str):
    state = {"query": query, "messages": [], "context": "", "domain": ""}
    final_state = agent_app.invoke(state)
    domain = final_state.get("domain", "custom")
    reply = final_state["messages"][-1].content if final_state["messages"] else "I'm sorry, I couldn't process that."
    return {"reply": reply, "domain": domain}
