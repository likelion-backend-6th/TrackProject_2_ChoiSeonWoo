from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import (
    TokenObtainPairView_,
    TokenRefreshView_,
    SignUpView,
    LoginView,
    UserViewSet,
    ProfileView,
    FollowListView,
)

router = DefaultRouter()
router.register("", UserViewSet, basename="user")
# router.register("path명", ViewSet클래스, basename="basename지정")

urlpatterns = [
    path("token/", TokenObtainPairView_.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView_.as_view(), name="token_refresh"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("<int:user_pk>/profile/", ProfileView.as_view(), name="user-profile"),
    path("follow/", FollowListView.as_view(), name="user-follow-list"),
    path("", include(router.urls)),
]
