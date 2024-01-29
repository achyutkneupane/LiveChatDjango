from rest_framework import serializers
from .models import Chatbox


class ChatboxSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chatbox
        fields = '__all__'

    def create(self, validated_data):
        return Chatbox.objects.create(**validated_data)
