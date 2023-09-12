from django.urls import include, path
from rest_framework.routers import DefaultRouter

from posts.views import PostViewSet

router = DefaultRouter()
router.register("", PostViewSet, basename="post")
# router.register("path명", ViewSet클래스, basename="basename지정")

urlpatterns = [
    path("", include(router.urls)),
]
