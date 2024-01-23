from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import User, Login
from .serializers import UserSerializer, LoginSerializer


@api_view(['GET'])
def index(request):
    return Response({'message': 'This is the main page'})


@api_view(['POST'])
def register(request):
    UserSerializer(data=request.data).is_valid(raise_exception=True).save()
    return Response({'message': 'User Registered Successfully'}, 200)
