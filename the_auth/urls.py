from django.urls import path
from .views import CurrentUserView, TheAuthRegisterView, TheAuthLoginView

urlpatterns = [
    # path('', TheAuthAPIView.as_view({'get': 'index'}), name='auth'),
    path('register', TheAuthRegisterView.as_view({'post': 'register'}), name='register'),
    path('login', TheAuthLoginView.as_view({'post': 'login'}), name='login'),
    path('get-user', CurrentUserView.as_view({'get': 'get_user'}), name='get-user'),
]
