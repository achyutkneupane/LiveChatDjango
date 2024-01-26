from rest_framework.permissions import IsAuthenticated


class AllowUnauthenticated(IsAuthenticated):
    def has_permission(self, request, view):
        return True


class MustBeAuthenticated(IsAuthenticated):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
