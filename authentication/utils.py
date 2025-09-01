import jwt
from datetime import datetime, timedelta
from server import settings
from django.contrib.auth.hashers import make_password, check_password
from user.models import User
from rest_framework.exceptions import AuthenticationFailed

SECRET_KEY = settings.JWT_SIGNATURE_KEY

# To handle jwt token

def generate_tokens(user):
    payload = {
        'id': str(user['id']),
        'username': user['username'],
        'email': user['email'],
        'role': user['role'],
        'exp': datetime.utcnow() + timedelta(days=1), # minutes=15
    }
    access_token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

    refresh_payload = {
        'id': user['id'],
        'exp': datetime.utcnow() + timedelta(days=7),
    }
    refresh_token = jwt.encode(refresh_payload, SECRET_KEY, algorithm='HS256')

    return access_token, refresh_token

def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user = User.objects.get(id=payload['id'])
        return user
    except (jwt.ExpiredSignatureError, jwt.DecodeError, User.DoesNotExist):
        return None

# To handle password

def encrypt_password(raw_password):
    return make_password(raw_password)

def check_encrypted_password(entered_password, stored_hashed_password):
    return check_password(entered_password, stored_hashed_password)

def get_user_from_token(request):
    auth_header = request.META.get('HTTP_AUTHORIZATION', '')
    
    if not auth_header.startswith('Bearer '):
        raise AuthenticationFailed("Authorization header must start with 'Bearer '")
    
    token = auth_header.split(' ')[1]
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed("Token has expired")
    except jwt.InvalidTokenError:
        raise AuthenticationFailed("Invalid token")

    # You now have access to user info in the payload
    user_data = {
        'id': payload.get('id'),
        'username': payload.get('username'),
        'email': payload.get('email'),
        'role': payload.get('role'),
    }
    return user_data
