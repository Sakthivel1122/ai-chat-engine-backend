from rest_framework import serializers

class AIProfileSerializer(serializers.Serializer):
    id = serializers.CharField(required=False)
    name = serializers.CharField(required=True)
    system_prompt = serializers.CharField(required=True)
    config = serializers.DictField(required=False)
