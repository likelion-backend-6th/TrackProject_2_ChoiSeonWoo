from common.permissions import CustomReadOnly


class PostCustomReadOnly(CustomReadOnly):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if (
            view.action in self.SAFE_ACTIONS
            or user.is_admin == True
            or (self.class_name(obj) == "Post" and obj.author == user)
        ):
            return True
        return False
