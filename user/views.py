from django.shortcuts import render
from rest_framework.views import APIView
from user.models import User
from server.utils import response
import json
from mongoengine.errors import DoesNotExist
from .serializers import CreateUserSerializer, UserSerializer

class UserCrud(APIView):
    def post(self, request):
        data = request.data.copy()
        # print('user_data', json.loads(request.body))
        # json_data = '{"username": "john_doe", "email": "john@example.com"}'
        # python_dict = json.loads(json_data)
        # print(python_dict)
        serializer = CreateUserSerializer(data=data)

        if not serializer.is_valid(): 
            return response(serializer.errors, "Invaid input", 400)

        # user = User(username=data['username'], email=data['email'])
        # user.save()
        return response(None, "User Created Successfully", 200)
    
    def get(self, request):
        try:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)

            # user_list = [
            #     {
            #         'id': str(user.id),
            #         'username': user.username,
            #         'email': user.email
            #     } for user in users
            # ]

            # users2 = []
            # for user in users:
            #     users2.append({
            #         'id': str(user.id),
            #         'username': user.username,
            #         'email': user.email
            #     })
            
            return response(serializer.data,"success", 200)

        except DoesNotExist:
            return response(None,"User not found", 400)
        except Exception as e:
            return response(None,"Error" + str(e), 400)
