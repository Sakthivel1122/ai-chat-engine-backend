import jwt
from rest_framework import authentication, exceptions
from django.conf import settings
from user.models import User
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied, NotAuthenticated
from server.settings import JWT_SIGNATURE_KEY
from server.utils import response

class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return None

        try:
            token_type, token = auth_header.split()
            if token_type.lower() != 'bearer':
                raise exceptions.AuthenticationFailed("Invalid token prefix")
        except ValueError:
            raise exceptions.AuthenticationFailed("Invalid Authorization header format")

        try:
            payload = jwt.decode(token, JWT_SIGNATURE_KEY, algorithms=["HS256"])
            user = User.objects.get(id=payload['id'], deleted_at=None)
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Token expired")
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed("Invalid token")
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed("User not found")

        return (user, token)

def custom_exception_handler(exc, context):
    from rest_framework.views import exception_handler
    api_response = exception_handler(exc, context)

    if isinstance(exc, NotAuthenticated):
        return response(None, "Authentication credentials were not provided.", 401)

    if isinstance(exc, AuthenticationFailed):
        return response(None, str(exc), 401)
    
    if isinstance(exc, PermissionDenied):
        return response(None, "You are not authorized to perform this action", 401)
    
    return api_response
 