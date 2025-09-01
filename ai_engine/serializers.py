from rest_framework import serializers
from .models import User

class AIProfileSerializer(serializers.Serializer):
    id = serializers.CharField(required=False)
    name = serializers.CharField(required=True)
    system_prompt = serializers.CharField(required=True)
    config = serializers.DictField(required=False)
    is_active = serializers.BooleanField(required=False)

class ChatSessionSerializer(serializers.Serializer):
    id = serializers.CharField(required=False)
    user_id = serializers.CharField(required=True)
    ai_profile_id = serializers.CharField(required=True)
    title = serializers.CharField(required=False)

class ChatSessionDocumentSerializer(serializers.Serializer):
    id = serializers.CharField(required=True)
    user = serializers.CharField(required=True)
    ai_profile = serializers.CharField(required=True)
    title = serializers.CharField(required=False)

    def to_representation(self, instance):
        return {
            "session_id": str(instance.id),
            # "user_id": str(instance.user.id) if instance.user else None,
            "ai_profile_id": str(instance.ai_profile.id) if instance.ai_profile else None,
            "title": instance.title,
        }

class ChatMessageSerializer(serializers.Serializer):
    chat_session_id = serializers.CharField(required=False)
    message = serializers.CharField(required=True)
    ai_profile_id = serializers.CharField(required=False)
