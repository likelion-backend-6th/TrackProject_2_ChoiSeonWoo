from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.request import Request
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema

from django_filters.rest_framework import DjangoFilterBackend

from posts.models import Comment, Post
from posts.serializers import CommentSerializer, PostSerializer
from posts.filters import PostFilter, CommentFilter
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


@extend_schema(tags=["06. Comment"])
class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [CommonUserPermission]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filterset_class = CommentFilter

    def get_queryset(self):
        post_pk = self.kwargs["post_pk"]
        queryset = Comment.objects.filter(post__pk=post_pk)
        comment_pk = self.kwargs.get("id")
        if comment_pk:
            queryset = queryset.filter(id=comment_pk)

        return queryset

    def list(self, request: Request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        post_pk = kwargs.get("post_pk")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data["post_id"] = post_pk
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["01. My - Comment"])
class MyCommentListView(APIView):
    serializer_class = CommentSerializer
    filter_backends = DjangoFilterBackend
    filterset_class = CommentFilter

    def get(self, request):
        user: User = request.user
        posts = user.comments.all()
        queryset = self.filter_backends().filter_queryset(request, posts, self)

        serializer = self.serializer_class(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
