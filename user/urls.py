from django.urls import path
from . import views

urlpatterns = [
    path("", views.UserCrud.as_view(), name="crud user"),
    # path("get/<str:user_id>", views.UserCrud.as_view(), name="crud user"),
]