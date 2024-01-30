from rest_framework import serializers
from .models import Chatbox


class ChatboxSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chatbox
        fields = '__all__'

    def create(self, validated_data):
        request = self.context['request']
        user = request.user
        name = validated_data.get('name')
        participants = validated_data.get('participants')

        participants_with_user_id = [user.id] + participants

        chatbox = Chatbox.objects.create(name=name)
        chatbox.participants.set(participants_with_user_id)

        return chatbox
