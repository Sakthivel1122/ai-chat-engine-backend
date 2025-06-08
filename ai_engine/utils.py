from langchain.schema import HumanMessage, AIMessage
from .models import ChatMessage, ChatSession
        
def load_chat_history(session_id, chat_engine):
    chat_session = ChatSession.objects(id=session_id, deleted_at=None).first()
    if not chat_session:
        raise ValueError("ChatSession not found")

    messages = ChatMessage.objects(session=chat_session).order_by("created_at")

    history = []
    for msg in messages:
        if msg.sender == "human":
            history.append(HumanMessage(content=msg.message))
        elif msg.sender == "bot":
            history.append(AIMessage(content=msg.message))

    chat_engine.set_history(history)
