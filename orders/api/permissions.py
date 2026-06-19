from rest_framework import permissions


class IsCustomUser(permissions.BasePermission):
    """Custom permission to allow only users with type 'customer' to create orders."""

    def has_permission(self, request, view):
        return request.user.type == "customer"


class IsBusinessUser(permissions.BasePermission):
    """Custom permission to allow only users with type 'business' to view orders."""

    def has_permission(self, request, view):
        return request.user.type == "business"
