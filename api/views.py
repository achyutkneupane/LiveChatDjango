from rest_framework.response import Response
from rest_framework.decorators import api_view
from .permissions import is_guest, logged_in
from .serializers import UserSerializer, LoginSerializer


@api_view(['GET'])
def index(request):
    if not logged_in(request):
        return Response({'message': 'You are not logged in'}, 401)
    return Response({'message': 'This is the main page'})


@api_view(['POST'])
def register(request):
    if logged_in(request):
        return Response({'message': 'You are already logged in'}, 400)

    serializer = UserSerializer(data=request.data)
    if not serializer.is_valid(raise_exception=True):
        return Response({'message': 'Invalid Data'}, 400)
    serializer.save()
    return Response({'message': 'User Registered Successfully'}, 200)
