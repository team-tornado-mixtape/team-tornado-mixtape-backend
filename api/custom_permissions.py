from rest_framework import permissions

class IsCreatorOrReadOnly(permissions.BasePermission):
    message = 'Editing MixTapes is restricted to the creator only.'

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if obj.creator == request.user:
            return True
        return False