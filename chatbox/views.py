from rest_framework.viewsets import ViewSet

class ChatboxView(ViewSet):
    def index(self, request):
        return Response({'message': 'This is the main page'}