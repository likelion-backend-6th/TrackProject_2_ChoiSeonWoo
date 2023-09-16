from django.urls import include, path
from rest_framework.routers import DefaultRouter

from posts.views import (
    PostViewSet,
    OtherPostListView,
    MyPostListView,
)

router = DefaultRouter()
router.register("", PostViewSet, basename="post")
# router.register("path명", ViewSet클래스, basename="basename지정")

urlpatterns = [
    path("others/", OtherPostListView.as_view(), name="other_posts_list"),
    path("my/", MyPostListView.as_view(), name="my_posts_list"),
    path("", include(router.urls)),
]
