from rest_framework import serializers
from .models import Chatbox


class ChatboxSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chatbox
        fields = '__all__'

    def create(self, validated_data):
        name = validated_data.get('name')
        participants = validated_data.get('participants')

        chatbox = Chatbox.objects.create(name=name)
        chatbox.participants.set(participants)

        return chatbox

    def update(self, instance, validated_data):
        name = validated_data.get('name')
        participants = validated_data.get('participants')

        instance.name = name
        instance.participants.set(participants)
        instance.save()

        return instance
