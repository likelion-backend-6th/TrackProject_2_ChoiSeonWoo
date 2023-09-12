from rest_framework.permissions import BasePermission
from rest_framework.exceptions import APIException
from rest_framework import status


class GenericAPIException(APIException):
    def __init__(self, status_code, detail=None, code=None):
        self.status_code = status_code
        super().__init__(detail=detail, code=code)


class CustomReadOnly(BasePermission):
    SAFE_ACTIONS = ("list",)
    message = "Not Allowed"

    @staticmethod
    def class_name(obj):
        return type(obj).__name__

    def has_permission(self, request, view):
        user = request.user
        if view.action in self.SAFE_ACTIONS:
            return True
        elif user.is_authenticated:
            return True
        elif not user.is_authenticated:
            response = {
                "detail": "Please log in to use the service.",
            }
            raise GenericAPIException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail=response
            )
        return False

    def has_object_permission(self, request, view, obj):
        user = request.user
        if (
            view.action in self.SAFE_ACTIONS
            or user.is_admin == True
            or (self.class_name(obj) == "User" and obj.email == user.email)
        ):
            return True
        return False
