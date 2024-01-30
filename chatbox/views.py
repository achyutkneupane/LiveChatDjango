from drf_yasg import openapi
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from LiveChat.responses import error_response
from rest_framework.response import Response
from .models import Chatbox, Message
from .serializers import ChatboxSerializer
from the_auth.permissions import logged_in


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
        }
    )
    def get(self, request):
        if not logged_in(request):
            return Response({'message': 'User not logged in', 'status': 400}, 400)
        chatboxes = Chatbox.objects.all()
        serializer = ChatboxSerializer(chatboxes, many=True)
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
        request_body=ChatboxSerializer
    )
    def post(self, request):
        if not logged_in(request):
            return Response({'message': 'User not logged in', 'status': 400}, 400)
        serializer = ChatboxSerializer(data=request.data)
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
        }
    )
    def get(self, request, pk):
        if not logged_in(request):
            return Response({'message': 'User not logged in', 'status': 400}, 400)
        try:
            chatbox = Chatbox.objects.get(pk=pk)
        except Chatbox.DoesNotExist:
            return Response({'message': 'Chatbox not found', 'status': 400}, 400)
        serializer = ChatboxSerializer(chatbox)
        return Response({'message': 'Chatbox fetched successfully', 'data': serializer.data, 'status': 200}, 200)


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
        }
    )
    def post(self, request, pk):
        if not logged_in(request):
            return Response({'message': 'User not logged in', 'status': 400}, 400)
        try:
            chatbox = Chatbox.objects.get(pk=pk)
        except Chatbox.DoesNotExist:
            return Response({'message': 'Chatbox not found', 'status': 400}, 400)
        message = Message.objects.create(chatbox=chatbox, message=request.data['message'])
        serializer = ChatboxSerializer(chatbox)
        return Response({'message': 'Message sent successfully', 'status': 200}, 200)
