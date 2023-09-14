from django.urls import include, path
from rest_framework.routers import DefaultRouter

from posts.views import PostViewSet, PostInfoView, MyPostView

router = DefaultRouter()
router.register("", PostViewSet, basename="post")
# router.register("path명", ViewSet클래스, basename="basename지정")

urlpatterns = [
    path("others/", PostInfoView.as_view(), name="other_users_posts"),
    path("my/", MyPostView.as_view(), name="my_posts_list"),
    path("my/<int:id>", MyPostView.as_view(), name="my_posts_detail"),
    path("", include(router.urls)),
]
