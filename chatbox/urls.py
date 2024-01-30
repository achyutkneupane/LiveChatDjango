from django.urls import path

from chatbox.views import ChatboxListView, ChatBoxView, SendMessageView

urlpatterns = [
    path('', ChatboxListView.as_view(), name='index'),
    path('<int:pk>', ChatBoxView.as_view(), name='show'),
    path('<int:pk>/message', SendMessageView.as_view(), name='message')
]
