from rest_framework import permissions


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        try:
            return request.user == obj.user
        except NameError:
            return False


class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_student


class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_teacher


class IsNotGuest(permissions.BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_guest

class IsGuest(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_guest
