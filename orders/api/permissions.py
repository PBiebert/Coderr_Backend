from rest_framework import permissions


class IsCustomUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.type == "customer"
