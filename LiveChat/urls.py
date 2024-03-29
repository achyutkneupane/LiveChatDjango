from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib import admin


schema_view = get_schema_view(
    openapi.Info(
        title="Live Chat API",
        default_version='v1',
        description="Live Chat API created for Applied Programming Project",
        contact=openapi.Contact(email="achyutkneupane@gmail.com"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny]
)

urlpatterns = [
    path('admin', admin.site.urls),

    path('api/', include([
        path('auth/', include('the_auth.urls'), name='auth'),
        path('chatbox/', include('chatbox.urls'), name='chatbox'),
    ]), name='api'),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
