from django.shortcuts import render
from server.utils import response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from .serializers import AIProfileSerializer, ChatSessionSerializer, ChatMessageSerializer, ChatSessionDocumentSerializer
from .models import AIProfile, ChatSession, ChatMessage
from authentication.permissions import IsAdmin, IsUser, IsUserOrAdmin
from user.models import User
from .utils import load_chat_history
from .ai_chat_engine import ChatEngine
from mongoengine.errors import DoesNotExist
from authentication.utils import get_user_from_token
from bson import ObjectId

@api_view(['POST'])
# @authentication_classes([])  # Disables authentication
@permission_classes([IsUser])
def send_message(request):
    data = request.data.copy()
    serializer = ChatMessageSerializer(data=data)
    if not serializer.is_valid():
        return response(serializer.errors, "failed", 400)
    
    chat_session_id = data.get('chat_session_id')
    user_message = data['message']

    if chat_session_id:
        try:
            chat_session = ChatSession.objects.get(id=chat_session_id)
        except ChatSession.DoesNotExist:
            return response({'error': 'Invalid chat session ID.'},"Error fetching chat session", status=400)
        except Exception as e:
            return response({'error': 'Invalid chat session ID.'},"Error fetching chat session", status=400)
    else:
        user_data = get_user_from_token(request)
        ai_profile_id = data['ai_profile_id']
        ai_profile = AIProfile.objects.get(id=ai_profile_id, deleted_at=None)
        user = User.objects.get(id=user_data['id'], deleted_at=None)

        chat_session = ChatSession(
            user=user,
            ai_profile=ai_profile,
            title=ai_profile.name
        )
        chat_session.save()

    ai_profile = chat_session.ai_profile
    chat_engine = ChatEngine(
        system_prompt=ai_profile.system_prompt,
        config=ai_profile.config
    )
    load_chat_history(chat_session.id, chat_engine)

    # print(chat_engine.get_history())
    ai_response = chat_engine.chat(user_message)

    ChatMessage(session=chat_session, sender="human", message=user_message).save()
    ChatMessage(session=chat_session, sender="bot", message=ai_response).save()

    return response({
        "chat_session_id": str(chat_session.id),
        "user_message": user_message,
        "ai_response": ai_response
    }, "success", 200)

@api_view(['GET'])
@permission_classes([IsUser])
def get_chat_history(request, session_id):
    try:
        session = ChatSession.objects.get(id=session_id)
    except DoesNotExist:
        return response({'error': 'Session not found'}, "Failed",400)

    messages = ChatMessage.objects(session=session).order_by('created_at')

    chat_history = [
        {
            'sender': msg.sender,
            'message': msg.message,
            'created_at': msg.created_at.isoformat()
        } for msg in messages
    ]

    return response({'session_id': str(session.id), 'chat_history': chat_history},"Retrieved Successfully", 200)

class AIProfileListCreate(APIView):
    # permission_classes = [IsUser]
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsUserOrAdmin()]
        elif self.request.method == 'POST':
            return [IsAdmin()]
        return [IsUserOrAdmin()]

    def get(self, request):
        try:
            profiles = AIProfile.objects.filter(deleted_at=None)
            serializer = AIProfileSerializer(profiles, many=True) 
            return response(serializer.data, "Retrieved Successfully!", 200)
        except Exception as e:
            return response({"error": str(e)}, "Failed to retrieve", 400)
    

    def post(self, request):
        try:
            data = request.data.copy()
            serializer = AIProfileSerializer(data=request.data)
            if not serializer.is_valid():
                return response(serializer.errors, "failed", 400)
            ai_profile = AIProfile(
                name=data['name'],
                system_prompt=data['system_prompt'],
                config=data.get('config', {})
            )
            ai_profile.save()

            ai_profile_res = {
                "id": str(ai_profile.id),
                "name": ai_profile.name,
                "system_prompt": ai_profile.system_prompt,
                "config": ai_profile.config
            }
            return response(ai_profile_res, "Created Successfully!", 200)
        except Exception as e:
            return response({"error": str(e)}, "Failed to create", 400)

@api_view(['POST'])
@permission_classes([IsUser])
def create_chat_session(request):
    data = request.data.copy()
    serializer = ChatSessionSerializer(data=data)

    if not serializer.is_valid():
        return response(serializer.errors, "Failed to create session", 400)
    
    ai_profile = AIProfile.objects.get(id=data['ai_profile_id'], deleted_at=None)
    user = User.objects.get(id=data['user_id'], deleted_at=None)
    chat_session = ChatSession(
        user=user,
        ai_profile=ai_profile,
        title=ai_profile.name
    )
    chat_session.save()

    chat_session_res = {
        "id": str(chat_session.id),
        # "user": {
        #     "id": str(chat_session.user.id),
        #     "name": chat_session.user.name,
        #     "email": chat_session.user.email,
        # },
        "ai_profile": {
            "id": str(chat_session.ai_profile.id),
            "name": chat_session.ai_profile.name,
            # "description": chat_session.ai_profile.description,
        }
    }
    return response(chat_session_res, "Chat Session Created Successfully", 200)

@api_view(['GET'])
@permission_classes([IsUser])
def get_chat_session(request):
    user_data = get_user_from_token(request)
    user_id = user_data['id']

    try:
        chat_sessions = ChatSession.objects(
            user=ObjectId(user_id),
            deleted_at=None
        )
    except Exception as e:
        return response({'error': str(e)}, "Error Retrieving Chat Session!", 400)

    chat_sessions_list = ChatSessionDocumentSerializer(chat_sessions, many=True)
    return response(chat_sessions_list.data, "Retrieved Successfully!", 200)
