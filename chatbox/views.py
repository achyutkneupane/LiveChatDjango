from drf_yasg import openapi
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from LiveChat.responses import error_response
from rest_framework.response import Response
from .models import Chatbox, Message
from the_auth.models import User
from .serializers import ChatboxSerializer, MessageSerializer
from the_auth.permissions import logged_in
import datetime


class ChatboxListView(APIView):
    @swagger_auto_schema(
        responses={
            400: error_response[400],
            200: openapi.Response('Chatboxes retrieved successfully', openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING),
                    'status': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'data': openapi.Schema(type=openapi.TYPE_ARRAY, items=Chatbox.schema())
                }
            ))
        },
        security=[{'Bearer': []}]
    )
    def get(self, request):
        if not logged_in(request):
            return Response({'message': 'User not logged in', 'status': 400}, 400)
        chatboxes = Chatbox.objects.all()
        serializer = ChatboxSerializer(chatboxes, many=True, context={'request': request})
        # update name
        for chatbox in serializer.data:
            participants = chatbox['participants']
            except_me = []
            for participant in participants:
                if participant != request.user.id:
                    except_me.append(participant)
            chatbox['name'] = chatbox['name'] or ', '.join(
                User.objects.filter(id__in=except_me).values_list('username', flat=True)
            ) or 'achyut'
        return Response({'message': 'Chatboxes retrieved successfully', 'data': serializer.data, 'status': 200}, 200)

    @swagger_auto_schema(
        responses={
            400: error_response[400],
            200: openapi.Response('Chatbox created successfully', openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING),
                    'status': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'data': Chatbox.schema()
                }
            ))
        },
        request_body=ChatboxSerializer,
        security=[{'Bearer': []}]
    )
    def post(self, request):
        if not logged_in(request):
            return Response({'message': 'User not logged in', 'status': 400}, 400)
        serializer = ChatboxSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid(raise_exception=True):
            return Response({'message': 'Invalid Data', 'status': 400}, 400)
        serializer.save()
        return Response({'message': 'Chatbox created successfully', 'data': serializer.data, 'status': 200}, 200)


class ChatBoxView(APIView):
    @swagger_auto_schema(
        responses={
            400: error_response[400],
            200: openapi.Response('Chatbox fetched successfully', openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING),
                    'status': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'data': Chatbox.schema()
                }
            ))
        },
        security=[{'Bearer': []}]
    )
    def get(self, request, pk):
        if not logged_in(request):
            return Response({'message': 'User not logged in', 'status': 400}, 400)
        try:
            chatbox = Chatbox.objects.get(pk=pk)
        except Chatbox.DoesNotExist:
            return Response({'message': 'Chatbox not found', 'status': 400}, 400)
        serializer = ChatboxSerializer(chatbox, context={'request': request})
        messages = Message.objects.filter(chatBox_id=pk)

        unread_messages = messages.filter(readAt__isnull=True).exclude(sender_id=request.user.id)
        now_with_tz = datetime.datetime.now(datetime.timezone.utc)
        unread_messages.update(readAt=now_with_tz)

        return_data = serializer.data
        return_data['messages'] = MessageSerializer(messages, many=True, context={'request': request}).data
        return_data['name'] = chatbox.name or "achyut"
        return Response({'message': 'Chatbox fetched successfully', 'data': return_data, 'status': 200}, 200)


class SendMessageView(APIView):
    @swagger_auto_schema(
        responses={
            400: error_response[400],
            200: openapi.Response('Message sent successfully', openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING),
                    'status': openapi.Schema(type=openapi.TYPE_INTEGER)
                }
            ), examples={
                'application/json': {
                    'message': 'Message sent successfully',
                    'status': 200
                }
            })
        },
        request_body=MessageSerializer,
        security=[{'Bearer': []}]
    )
    def post(self, request, pk):
        if not logged_in(request):
            return Response({'message': 'User not logged in', 'status': 400}, 400)
        try:
            Chatbox.objects.get(pk=pk)
        except Chatbox.DoesNotExist:
            return Response({'message': 'Chatbox not found', 'status': 400}, 400)
        message_serializer = MessageSerializer(data=request.data, context={'request': request, 'pk': pk})
        if not message_serializer.is_valid(raise_exception=True):
            return Response({'message': 'Invalid Data', 'status': 400}, 400)
        message_serializer.save()
        return Response({'message': 'Message sent successfully', 'status': 200}, 200)
