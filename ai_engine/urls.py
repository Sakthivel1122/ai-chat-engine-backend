from django.urls import path
from . import views

urlpatterns = [
    path("api/v1/user/send-message", views.send_message, name="ask question"),
    path("api/v1/user/chat-history/<str:session_id>/", views.get_chat_history, name="ask question"),
    path("api/v1/user/get-chat-session", views.get_chat_session, name="ask question"),
    path("api/v1/user/get-chat-session-data", views.get_session_data, name="ask question"),
    path("api/v1/user/create-chat-session", views.create_chat_session, name="create chat session"),
    path("api/v1/user/ai-profile", views.AIProfileCRUD.as_view(), name="get all ai profiles"),
    path("api/v1/user/ai-profile/<str:ai_profile_id>/", views.AIProfileCRUD.as_view(), name="get all ai profiles"),
    path("api/v1/admin/ai-profile", views.AIProfileCRUD.as_view(), name="crud ai profile"),
    path("api/v1/admin/default-ai-profile", views.DefaultAIProfileCRUD.as_view(), name="crud ai profile"),
]
