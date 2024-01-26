from rest_framework.permissions import IsAuthenticated


class CustomIsAuthenticated(IsAuthenticated):
    def has_permission(self, request, view):
        if view.action == 'token_obtain_pair' or view.action == 'token_refresh':
            return True
        return super().has_permission(request, view)
