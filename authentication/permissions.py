from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == "admin"

class IsUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, 'role', None) == "user"

class IsUserOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role in ["user", "admin"] 
