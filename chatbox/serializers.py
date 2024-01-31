from rest_framework import serializers
from .models import Chatbox, Message
from the_auth.models import User
from django.db.models import Q


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
        return last_message.readAt is None and last_message.sender_id != self.context['request'].user.id if last_message else False

    def create(self, validated_data):
        try:
            request = self.context['request']
            user = request.user
            name = validated_data.get('name')
            participants = validated_data.get('participants')
        except Exception as e:
            raise serializers.ValidationError({'message': e, 'status': 400}, 400)

        participants_with_user_id = [user.id] + participants

        query = Q(participants__exact=participants_with_user_id[0], name__isnull=True)
        for participant_id in participants_with_user_id[1:]:
            query |= Q(participants__exact=participant_id, name__isnull=True)

        chatbox_with_same_participants = Chatbox.objects.filter(query).distinct()
        if chatbox_with_same_participants:
            return_value = chatbox_with_same_participants.first()
            return return_value

        chatbox = Chatbox.objects.create(name=name)
        chatbox.participants.set(participants_with_user_id)

        return chatbox


class MessageSerializer(serializers.ModelSerializer):

    sender = serializers.SerializerMethodField()
    senderName = serializers.SerializerMethodField()
    chatBox = serializers.SerializerMethodField()
    isMe = serializers.SerializerMethodField()

    def get_sender(self, obj):
        return obj.sender_id

    def get_senderName(self, obj):
        return obj.sender.username

    def get_chatBox(self, obj):
        return obj.chatBox_id

    def get_isMe(self, obj):
        return obj.sender_id == self.context['request'].user.id

    class Meta:
        model = Message
        fields = ['id', 'content', 'createdAt', 'updatedAt', 'sender', 'senderName', 'chatBox', 'replyTo', 'isForwarded', 'isMe']

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
