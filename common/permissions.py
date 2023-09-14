from rest_framework.permissions import BasePermission
from rest_framework.exceptions import APIException
from rest_framework import status


class GenericAPIException(APIException):
    def __init__(self, status_code, detail=None, code=None):
        self.status_code = status_code
        super().__init__(detail=detail, code=code)


class IsAdminOrReadOnly(BasePermission):
    SAFE_METHODS = ("GET",)
    message = "Not Allowed"

    @staticmethod
    def class_name(obj):
        return type(obj).__name__

    def has_permission(self, request, view):
        user = request.user
        if request.method in self.SAFE_METHODS:
            return True
        elif user.is_admin:
            return True
        elif not user.is_admin:
            response = {
                "detail": "Administrator privileges required",
            }
            raise GenericAPIException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail=response
            )
        return False

    def has_object_permission(self, request, view, obj):
        user = request.user
        if request.method in self.SAFE_METHODS:
            return True
        elif user.is_admin:
            return True
        return False


class CustomReadOnly(BasePermission):
    SAFE_METHODS = ("GET",)
    attributes_to_check = ("email", "user", "user_from", "author")
    message = "Not Allowed"

    @staticmethod
    def class_name(obj):
        return type(obj).__name__

    def has_permission(self, request, view):
        user = request.user
        if request.method in self.SAFE_METHODS:
            return True
        elif user.is_authenticated:
            return True
        elif not user.is_authenticated:
            response = {
                "detail": "Please login to use the service.",
            }
            raise GenericAPIException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail=response
            )
        return False

    def has_object_permission(self, request, view, obj):
        user = request.user
        if request.method in self.SAFE_METHODS:
            return True
        if self.class_name(obj) == "User" and obj.email == user.email:
            return True
        for attr in self.attributes_to_check:
            if hasattr(obj, attr):
                attr_value = getattr(obj, attr)
                if user == attr_value:
                    return True
                return False
        return False
