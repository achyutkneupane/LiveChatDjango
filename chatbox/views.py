from drf_yasg import openapi
from rest_framework.viewsets import ViewSet
from drf_yasg.utils import swagger_auto_schema
from LiveChat.responses import error_response
from rest_framework.response import Response


class ChatboxView(ViewSet):
    @swagger_auto_schema(responses={
        400: error_response[400]
    })
    def index(self, request):
        return Response({'message': 'This is the main page'}, 200)
