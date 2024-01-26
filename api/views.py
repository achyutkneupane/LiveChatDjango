from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import User, Login
from .serializers import UserSerializer, LoginSerializer


@api_view(['GET'])
def index(request):
    return Response({'message': 'This is the main page'})


@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if not serializer.is_valid(raise_exception=True):
        return Response({'message': 'Invalid Data'}, 400)
    serializer.save()
    return Response({'message': 'User Registered Successfully'}, 200)
