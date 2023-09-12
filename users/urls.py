from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import (
    FollowViewSet,
    ProfileViewSet,
    SignUpView,
    LoginView,
    UserViewSet,
    TokenObtainPairView_,
    TokenRefreshView_,
)

router = DefaultRouter()
router.register("profiles", ProfileViewSet, basename="profile")
router.register("follows", FollowViewSet, basename="follow")
router.register("", UserViewSet, basename="user")
# router.register("path명", ViewSet클래스, basename="basename지정")

urlpatterns = [
    path("token/", TokenObtainPairView_.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView_.as_view(), name="token_refresh"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("", include(router.urls)),
]
