from rest_framework import serializers

class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    role = serializers.CharField()
    provider = serializers.CharField()
    created_at = serializers.DateTimeField()
