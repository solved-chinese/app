from rest_framework import permissions


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        try:
            return request.user == obj.user
        except NameError:
            return False
