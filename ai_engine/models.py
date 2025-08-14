from mongoengine import ReferenceField, StringField, DictField, BooleanField
from server.models import TimeStampedDocument
from user.models import User

class AIProfile(TimeStampedDocument):
    name = StringField(required=True)  # e.g., Resume Reviewer, Interview Coach
    system_prompt = StringField(required=True)
    config = DictField(default=dict)  # Optional: model type, temperature, max_tokens, etc.
    is_default = BooleanField(default=False)
    is_active = BooleanField(default=False)

    meta = {'collection': 'ai_profiles'}

class ChatSession(TimeStampedDocument):
    user = ReferenceField(User, required=True)
    ai_profile = ReferenceField(AIProfile, required=True)
    title = StringField()  # optional title for the chat

    meta = {'collection': 'chat_sessions'}

class ChatMessage(TimeStampedDocument):
    session = ReferenceField(ChatSession, required=True)
    sender = StringField(required=True, choices=["human", "bot"])
    message = StringField(required=True)

    meta = {'collection': 'chat_messages'}
