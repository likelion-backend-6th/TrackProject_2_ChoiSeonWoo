from django.urls import include, path

from rest_framework.routers import SimpleRouter

from rest_framework_nested.routers import NestedDefaultRouter

from posts.views import (
    CommentViewSet,
    ImageViewSet,
    PostViewSet,
)

router = SimpleRouter()
router.register("", PostViewSet, basename="post")
comment_router = NestedDefaultRouter(router, "", lookup="post")
comment_router.register("comments", CommentViewSet, basename="post-comments")
image_router = NestedDefaultRouter(router, "", lookup="post")
image_router.register("images", ImageViewSet, basename="post-images")
# router.register("path명", ViewSet클래스, basename="basename지정")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(comment_router.urls)),
    path("", include(image_router.urls)),
]
