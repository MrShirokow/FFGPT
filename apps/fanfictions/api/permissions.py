from django.http import HttpRequest

from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Object-level permission to only allow owners of an object to edit it.

    Assumes the model instance has an `user` attribute.

    """

    # pylint: disable=unused-argument
    def has_object_permission(self, request: HttpRequest, view, obj) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user_id == request.user.id
