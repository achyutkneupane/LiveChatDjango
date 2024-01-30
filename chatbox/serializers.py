from rest_framework import serializers
from .models import Chatbox, Message


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


class ChatboxMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = '__all__'

    def create(self, validated_data):
        request = self.context['request']
        sender = request.user
        content = validated_data.get('content')
        chatbox = validated_data.get('chatBox')
        reply_to = validated_data.get('replyTo', None)
        is_forwarded = validated_data.get('isForwarded', False)

        message = Message.objects.create(
            sender=sender,
            content=content,
            chatBox=chatbox,
            replyTo=reply_to,
            isForwarded=is_forwarded
        )

        return message
