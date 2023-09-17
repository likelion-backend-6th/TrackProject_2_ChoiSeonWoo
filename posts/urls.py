from django.urls import include, path

from rest_framework.routers import SimpleRouter

from rest_framework_nested.routers import NestedDefaultRouter

from posts.views import (
    CommentViewSet,
    ImageViewSet,
    MyImageListView,
    PostViewSet,
    OtherPostListView,
    MyPostListView,
    OtherImageListView,
    MyCommentListView,
)

router = SimpleRouter()
router.register("", PostViewSet, basename="post")
comment_router = NestedDefaultRouter(router, "", lookup="post")
comment_router.register("comments", CommentViewSet, basename="post-comments")
image_router = NestedDefaultRouter(router, "", lookup="post")
image_router.register("images", ImageViewSet, basename="post-images")
# router.register("path명", ViewSet클래스, basename="basename지정")

urlpatterns = [
    path("others/", OtherPostListView.as_view(), name="other_posts_list"),
    path("my/", MyPostListView.as_view(), name="my_posts_list"),
    path("comments/my/", MyCommentListView.as_view(), name="my_comments_list"),
    path("images/others/", OtherImageListView.as_view(), name="other_images_list"),
    path("images/my/", MyImageListView.as_view(), name="my_images_list"),
    path("", include(router.urls)),
    path("", include(comment_router.urls)),
    path("", include(image_router.urls)),
]
