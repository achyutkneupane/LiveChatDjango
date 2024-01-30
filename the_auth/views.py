from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .permissions import logged_in
from .serializers import UserSerializer, UserLoginSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from LiveChat.responses import login_response, error_response, register_response


class TheAuthAPIView(ViewSet):
    @swagger_auto_schema(responses={
        200: openapi.Response('This is the main page', openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'message': openapi.Schema(type=openapi.TYPE_STRING),
                'status': openapi.Schema(type=openapi.TYPE_INTEGER)
            }
        ), examples={
            'application/json': {
                'message': 'This is the main page',
                'status': 200
            }
        }),
        400: error_response[400]
    })
    def index(self, request):
        if not logged_in(request):
            return Response({'message': 'You are not logged in', 'status': 400}, 400)
        return Response({'message': 'This is the main page', 'status': 200}, 200)


class TheAuthRegisterView(ViewSet):
    @swagger_auto_schema(responses=register_response, request_body=UserSerializer)
    def register(self, request):
        if logged_in(request):
            return Response({'message': 'You are already logged in', 'status': 400}, 400)

        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({'message': 'Invalid Data', 'status': 400}, 400)
        serializer.save()
        return Response({'message': 'User Registered Successfully', 'data': serializer.data, 'status': 200}, 200)


class TheAuthLoginView(ViewSet):
    @swagger_auto_schema(responses=login_response, request_body=UserLoginSerializer)
    def login(self, request):
        if logged_in(request):
            return Response({'message': 'You are already logged in', 'status': 400}, 400)

        serializer = UserLoginSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({'message': 'Invalid Data', 'status': 400}, 400)

        login_serializer_data = {
            'user': serializer.validated_data.id,
            'userAgent': request.META.get('HTTP_USER_AGENT', 'Unknown User Agent'),
            'ipAddress': request.META.get('REMOTE_ADDR', 'Unknown IP Address')
        }

        login_serializer = LoginSerializer(data=login_serializer_data)

        if not login_serializer.is_valid(raise_exception=True):
            return Response({'message': 'Invalid Data', 'status': 400}, 400)

        login_serializer.save()

        refresh_token = RefreshToken.for_user(serializer.validated_data)
        return Response({
            'message': 'User Logged In Successfully',
            'data': {
                'access': str(refresh_token.access_token)
            },
            'status': 200
        }, 200)
