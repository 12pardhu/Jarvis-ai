from app.llm.ollama_client import ask_ollama as generate_response
from app.memory.vector_store import add_memory, search_memory
from app.memory.session_store import session_memory

def process_query(query: str, *, session_id: str | None = None) -> str:

    memories = search_memory(query)
    history = session_memory.get_context_text(session_id or "")

    prompt = f"""You are Jarvis, an intelligent assistant.

Use the provided memory snippets only if relevant. If they are irrelevant, ignore them.

Conversation so far (most recent last):
{history}

User query:
{query}

Memory snippets:
{memories}
"""

    response = generate_response(prompt)

    add_memory(query)
    if session_id:
        session_memory.add(session_id, "user", query)
        session_memory.add(session_id, "assistant", response)

    return response