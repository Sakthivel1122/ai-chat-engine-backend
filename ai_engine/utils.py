from langchain.schema import HumanMessage, AIMessage
from .models import ChatMessage, ChatSession
from .ai_chat_engine import ChatEngine
        
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

def get_chat_session_title_suggestion(user_message):
    system_prompt = '''
        You are a helpful assistant that generates short, relevant, and well-formatted titles for chat sessions. You will receive the first message from a user in a conversation with an AI assistant. Your goal is to summarize the main intent or topic of the message into a clear, concise title consisting of 3 to 6 words only.

        Formatting Rules (Strict):

        Do not include any prefix like “Title:” or “Output:” in your response.

        Do not include any punctuation (e.g., period, colon, question mark).

        Capitalize major words (title case).

        Do not wrap the title in quotes or backticks.

        Keep the title under 7 words.

        Be specific, informative, and creative.

        Avoid generic words like “Chat” or “Conversation”.

        Examples:

        User Message: How can I improve my resume for tech jobs?
        ✅ Correct: Optimizing Resume for Tech Roles
        ❌ Incorrect: Output: Optimizing Resume for Tech Roles
        ❌ Incorrect: Title: Optimizing Resume for Tech Roles

        User Message: I want a healthy Indian dinner recipe.
        ✅ Correct: Healthy Indian Dinner Ideas

        Return only the title as your output — nothing else.
    '''
    chat_engine = ChatEngine(
        system_prompt=system_prompt,
        config={}
    )
    ai_response = chat_engine.chat(user_message)
    return ai_response
