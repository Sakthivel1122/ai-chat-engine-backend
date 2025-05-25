from django.shortcuts import render
from rest_framework.views import APIView
from server.utils import response
from user.models import User
from .utils import generate_tokens
from django.forms.models import model_to_dict
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from .utils import encrypt_password, check_encrypted_password, get_user_from_token

@api_view(['POST'])
@authentication_classes([])  # Disables authentication
@permission_classes([AllowAny])
def user_signup(request):
    data = request.data.copy() 
    # Check if user exists using MongoEngine's query
    user_exists = User.objects(email=data['email'], deleted_at=None).first()
    if user_exists:
        return response(None, "User Already exists!", 400)

    try:
        encrypted_password = encrypt_password(data['password'])

        # Create new user using MongoEngine
        user = User(
            username=data['username'],
            email=data['email'],
            password=encrypted_password,
        )
        user.save()

        # Create user dict (MongoEngine doesn't have model_to_dict)
        user_dict = {
            "id": str(user.id),  # ObjectId must be stringified
            "username": user.username,
            "email": user.email,
            "role": user.role
        }

        try:
            access_token, refresh_token = generate_tokens(user_dict)
            return response({
                'user_data': user_dict,
                'token': {
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }
            }, "success", 200)
        except Exception as e:
            return response(None, "Failed to generate token", 400)

    except Exception as e:
        return response(None, f"Failed to create user! {str(e)}", 400)

@api_view(['POST'])
@authentication_classes([])  # Disables authentication
@permission_classes([AllowAny])
def user_login(request):
    data = request.data.copy()

    # Validate input
    if 'email' not in data or 'password' not in data:
        return response(None, "Mandatory key missing", 400)

    # MongoEngine query (check if user exists and not deleted)
    user = User.objects(email=data['email'], deleted_at=None).first()
    if not user:
        return response(None, "User not exist!", 400)

    # user_dict = user.to_mongo().to_dict()  # Convert MongoEngine document to dict
    # user_dict['id'] = str(user.id)  # Ensure ObjectId is stringified
    user_dict = {
        'id': str(user.id),
        'email': user.email,
        'username': user.username,
        'role': user.role
    }

    # Password check
    if not check_encrypted_password(data['password'], user.password):
        return response(None, "Password mismatch", 400)

    try:
        access_token, refresh_token = generate_tokens(user_dict)
        return response({
            'user_data': user_dict,
            'token': {
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        }, "success", 200)
    except Exception as e:
        return response(None, f"Failed to generate token: {str(e)}", 400)

@api_view(['POST'])
@authentication_classes([])  # Disables authentication
@permission_classes([AllowAny])
def create_admin(request):
    data = request.data.copy() 
    # Check if user exists using MongoEngine's query
    user_exists = User.objects(email=data['email'], role='admin', deleted_at=None).first()
    if user_exists:
        return response(None, "User Already exists!", 400)

    try:
        encrypted_password = encrypt_password(data['password'])

        # Create new user using MongoEngine
        user = User(
            username=data['username'],
            email=data['email'],
            password=encrypted_password,
            role='admin'
        )
        user.save()

        # Create user dict (MongoEngine doesn't have model_to_dict)
        user_dict = {
            "id": str(user.id),  # ObjectId must be stringified
            "username": user.username,
            "email": user.email,
            "role": user.role
        }

        try:
            access_token, refresh_token = generate_tokens(user_dict)
            return response({
                'user_data': user_dict,
                'token': {
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }
            }, "success", 200)
        except Exception as e:
            return response(None, "Failed to generate token", 400)

    except Exception as e:
        return response(None, f"Failed to create user! {str(e)}", 400)
    
@api_view(['GET'])
@authentication_classes([])  # Disables authentication
@permission_classes([AllowAny])
def refresh_token(request):
    user_data = get_user_from_token(request)

    user = User.objects(id=user_data['id'], deleted_at=None).first()
    if not user:
        return response(None, "User not exist!", 400)
    
    user_dict = {
        'id': str(user.id),
        'email': user.email,
        'username': user.username,
        'role': user.role
    }

    try:
        access_token, refresh_token = generate_tokens(user_dict)
        return response({
            'user_data': user_dict,
            'token': {
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        }, "success", 200)
    except Exception as e:
        return response(None, f"Failed to generate token: {str(e)}", 400)