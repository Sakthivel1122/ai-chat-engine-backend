from django.urls import path
from . import views

urlpatterns = [
    path("api/v1/signup", views.user_signup, name="signup"),
    path("api/v1/login", views.user_login, name="login"),
    path("api/v1/oauth-login", views.oauth_google_login, name="oauth login"),
    path("api/v1/refresh-token", views.refresh_token, name="refresh token"),
    path("api/v1/create-admin", views.create_admin, name="create admin"),
]
