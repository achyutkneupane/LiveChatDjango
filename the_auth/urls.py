from django.urls import path
from .views import TheAuthAPIView, TheAuthRegisterView, TheAuthLoginView

urlpatterns = [
    # path('', TheAuthAPIView.as_view({'get': 'index'}), name='auth'),
    path('register', TheAuthRegisterView.as_view({'post': 'register'}), name='register'),
    path('login', TheAuthLoginView.as_view({'post': 'login'}), name='login')
]
