from django.urls import path
from . import views

urlpatterns = [
    path("api/v1/dashboard", views.get_admin_dashboard, name="admin dashboard"),
    path("api/v1/messages-exchanged-per-day", views.MessagesExchangedCRUD.as_view(), name="admin dashboard"),
    path("api/v1/user", views.UserCRUD.as_view(), name="admin dashboard"),
]
