from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import (
    TokenObtainPairView_,
    TokenRefreshView_,
    SignUpView,
    LoginView,
    UserViewSet,
    ProfileViewSet,
    FollowViewSet,
    MyInfoView,
    OtherUserInfoView,
    ProfileView,
    OtherProfileView,
    FollowView,
    FollowingView,
    FollowerView,
    FeedView,
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
    path("my/", MyInfoView.as_view(), name="my_info"),
    path("others/", OtherUserInfoView.as_view(), name="other_users"),
    path("my/profile/", ProfileView.as_view(), name="my_profile"),
    path("others/profile/", OtherProfileView.as_view(), name="other_profile"),
    path("my/follow/<int:id>/", FollowView.as_view(), name="my_follow"),
    path("my/following/", FollowingView.as_view(), name="my_following"),
    path("my/follower/", FollowerView.as_view(), name="my_follower"),
    path("my/feed/", FeedView.as_view(), name="my_feed"),
    path("", include(router.urls)),
]
