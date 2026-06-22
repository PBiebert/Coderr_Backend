from rest_framework import permissions


class IsCustomUser(permissions.BasePermission):
    """Permission to allow only users with type 'customer' to create orders."""

    def has_permission(self, request, view):
        return request.user.type == "customer"


class IsReviewer(permissions.BasePermission):
    """Permission to allow only the reviewer to update or delete their review."""

    def has_object_permission(self, request, view, obj):
        return obj.reviewer == request.user
