from django.urls import path

from chatbox.views import ChatboxListView, ChatBoxView

urlpatterns = [
    path('', ChatboxListView.as_view(), name='index'),
    path('<int:pk>', ChatBoxView.as_view(), name='show')
]
