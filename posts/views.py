from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.request import Request
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema

from django_filters.rest_framework import DjangoFilterBackend

from posts.models import Post
from posts.serializers import PostSerializer
from posts.filters import PostFilter
from posts.permissions import CommonUserPermission
from users.models import User


@extend_schema(tags=["05. Post"])
class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [CommonUserPermission]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filterset_class = PostFilter

    def list(self, request: Request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["01. My - Post"])
class OtherPostListView(APIView):
    serializer_class = PostSerializer
    filter_backends = DjangoFilterBackend
    filterset_class = PostFilter

    def get(self, request):
        posts = Post.objects.exclude(author=request.user)
        queryset = self.filter_backends().filter_queryset(request, posts, self)

        serializer = self.serializer_class(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["01. My - Post"])
class MyPostListView(APIView):
    serializer_class = PostSerializer
    filter_backends = DjangoFilterBackend
    filterset_class = PostFilter

    def get(self, request):
        user: User = request.user
        posts = user.posts.all()
        queryset = self.filter_backends().filter_queryset(request, posts, self)

        serializer = self.serializer_class(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
