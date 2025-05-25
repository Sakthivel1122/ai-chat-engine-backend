from rest_framework import serializers
from .models import User

class CreateUserSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    age = serializers.IntegerField(required=False)  # Optional field

class UserSerializer(serializers.Serializer):
    id = serializers.CharField(source='pk')  # or source='id' if pk doesn't work
    username = serializers.CharField()
    email = serializers.EmailField()
    # age = serializers.EmailField(required=False)
