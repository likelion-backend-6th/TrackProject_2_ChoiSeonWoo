from common.permissions import CustomReadOnly


class UserCustomReadOnly(CustomReadOnly):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if (
            view.action in self.SAFE_ACTIONS
            or user.is_admin == True
            or (self.class_name(obj) == "User" and obj.email == user.email)
            or (self.class_name(obj) == "Profile" and obj.user == user)
            or (self.class_name(obj) == "Follow" and obj.user_from == user)
        ):
            return True
        return False
