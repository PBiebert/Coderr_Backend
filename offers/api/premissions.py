from rest_framework import permissions


class IsBusinessUser(permissions.BasePermission):
    """
    Custom permission to only allow business users to create offers.
    """

    def has_permission(self, request, view):
        return request.user.type == "business"
