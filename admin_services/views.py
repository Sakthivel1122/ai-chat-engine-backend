from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from authentication.permissions import IsAdmin
from user.models import User
from ai_engine.models import ChatSession, ChatMessage, AIProfile
from mongoengine.queryset.visitor import Q
from server.utils import response
from rest_framework.views import APIView
from .utils import get_daily_message_counts
from .serializers import UserSerializer

@api_view(['GET'])
@permission_classes([IsAdmin])
def get_admin_dashboard(request):
    try:
        user_count = User.objects(deleted_at=None, role='user').count()
        session_count = ChatSession.objects(deleted_at=None).count()
        chat_message_count = ChatMessage.objects(deleted_at=None).count()
        ai_profile_count = AIProfile.objects(Q(is_default__ne=True) | Q(is_default__exists=False), deleted_at=None).count()

        res_data = {
            'user_count': user_count,
            'session_count': session_count,
            'chat_message_count': chat_message_count,
            'ai_profile_count': ai_profile_count,
        }
        return response(res_data, "Retrieved Successfully", 200)
    except Exception as e:
        return response({'error': str(e)}, "Failed to retrieved", 400)

class MessagesExchangedCRUD(APIView):
    permission_classes = [IsAdmin]
    # def get_permissions(self):
    #     if self.request.method == 'GET':
    #         return [IsUserOrAdmin()]
    #     elif self.request.method == 'POST':
    #         return [IsAdmin()]
    #     elif self.request.method == 'DELETE':
    #         return [IsAdmin()]
    #     return [IsUserOrAdmin()]

    def post(self, request):
        try:
            data = request.data.copy()
            if 'days' in data:
                days = data['days']
            else:
                days = 7

            res_data = get_daily_message_counts(days)
            return response(res_data, "Retrieved Successfully", 200)
        except Exception as e:
            return response({'error': str(e)}, "Retrieved Successfully", 400)

class UserCRUD(APIView):
    permission_classes = [IsAdmin]
    # def get_permissions(self):
    #     if self.request.method == 'GET':
    #         return [IsUserOrAdmin()]
    #     elif self.request.method == 'POST':
    #         return [IsAdmin()]
    #     elif self.request.method == 'DELETE':
    #         return [IsAdmin()]
    #     return [IsUserOrAdmin()]

    def get(self, request):
        try:
            # data = request.data.copy()
            # if 'days' in data:
            #     days = data['days']
            # else:
            #     days = 7

            # res_data = get_daily_message_counts(days)

            users = User.objects(deleted_at=None, role='user')

            serializer = UserSerializer(users, many=True)

            return response(serializer.data, "Retrieved Successfully", 200)
        except Exception as e:
            return response({'error': str(e)}, "Retrieved Successfully", 400)
