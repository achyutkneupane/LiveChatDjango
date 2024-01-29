from django.urls import path

from chatbox.views import ChatboxView

urlpatterns = [
    path('', ChatboxView.as_view({'get': 'index'}), name='chatbox'),
]
