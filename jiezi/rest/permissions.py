from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsTeacher(BasePermission):
    message = 'Permission denied. Only teacher can access.'

    def has_permission(self, request, view):
        return request.user.is_teacher


class IsTeacherOrReadOnly(BasePermission):
    message = 'Permission denied. Only teacher has change permission.'

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_teacher

