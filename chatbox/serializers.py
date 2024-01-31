from rest_framework import serializers
from .models import Chatbox, Message


class ChatboxSerializer(serializers.ModelSerializer):

    lastMessage = serializers.SerializerMethodField()
    lastMessageTime = serializers.SerializerMethodField()
    iAmLastSender = serializers.SerializerMethodField()
    isUnread = serializers.SerializerMethodField()

    class Meta:
        model = Chatbox
        fields = '__all__'

    def get_lastMessage(self, obj):
        last_message = Message.objects.filter(chatBox_id=obj.id).order_by('-createdAt').first()
        return last_message.content if last_message else None

    def get_lastMessageTime(self, obj):
        last_message = Message.objects.filter(chatBox_id=obj.id).order_by('-createdAt').first()
        return last_message.createdAt if last_message else None

    def get_iAmLastSender(self, obj):
        last_message = Message.objects.filter(chatBox_id=obj.id).order_by('-createdAt').first()
        return last_message.sender_id == self.context['request'].user.id if last_message else None

    def get_isUnread(self, obj):
        last_message = Message.objects.filter(chatBox_id=obj.id).order_by('-createdAt').first()
        return last_message.readAt is None if last_message else False

    def create(self, validated_data):
        try:
            request = self.context['request']
            user = request.user
            name = validated_data.get('name')
            participants = validated_data.get('participants')
        except Exception as e:
            raise serializers.ValidationError({'message': e, 'status': 400}, 400)

        participants_with_user_id = [user.id] + participants

        chatbox = Chatbox.objects.create(name=name)
        chatbox.participants.set(participants_with_user_id)

        return chatbox


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'content', 'createdAt', 'updatedAt']

    def create(self, validated_data):
        try:
            request = self.context['request']
            content = validated_data.get('content')
            chatbox = self.context['pk']
            reply_to = validated_data.get('replyTo', None)
            is_forwarded = validated_data.get('isForwarded', False)

            message = Message.objects.create(
                sender_id=request.user.id,
                content=content,
                chatBox_id=chatbox,
                replyTo=reply_to,
                isForwarded=is_forwarded
            )
        except Exception as e:
            raise serializers.ValidationError({'message': e, 'status': 400}, 400)

        return message
