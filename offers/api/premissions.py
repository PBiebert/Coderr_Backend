from rest_framework import permissions


class IsBusinessUser(permissions.BasePermission):
    """
    Custom permission to only allow business users to create offers.
    """

    def has_permission(self, request, view):
        """Check if the user is a business user."""

        return request.user.type == "business"


class IsOwner(permissions.BasePermission):
    """Custom permission to only allow owners of an object to edit or delete it."""

    def has_object_permission(self, request, view, obj):
        """Check if the user is the owner of the object."""

        return obj.user == request.user
