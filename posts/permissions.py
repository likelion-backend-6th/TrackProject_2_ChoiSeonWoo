from common.permissions import IsAdminOrReadOnly


class CommonUserPermission(IsAdminOrReadOnly):
    SAFE_METHODS = (
        "GET",
        "POST",
        "PATCH",
    )
