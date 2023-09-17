from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType

from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.request import Request
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema

from django_filters.rest_framework import DjangoFilterBackend

from posts.models import Comment, Image, Like, Post
from posts.serializers import (
    CommentSerializer,
    ImageSerializer,
    PostSerializer,
)
from posts.filters import PostFilter, CommentFilter
from posts.permissions import CommonUserPermission
from users.models import User


@extend_schema(tags=["06. Post"])
class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [CommonUserPermission]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filterset_class = PostFilter

    def list(self, request: Request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["01. Others"])
class OtherPostListView(APIView):
    serializer_class = PostSerializer
    filter_backends = DjangoFilterBackend
    filterset_class = PostFilter

    def get(self, request):
        user: User = request.user
        posts = Post.objects.exclude(author=user)
        queryset = self.filter_backends().filter_queryset(request, posts, self)

        serializer = self.serializer_class(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["01. My"])
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


@extend_schema(tags=["07. Comment"])
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


@extend_schema(tags=["01. My"])
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


@extend_schema(tags=["08. Image"])
class ImageViewSet(viewsets.ModelViewSet):
    permission_classes = [CommonUserPermission]
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    def get_queryset(self):
        post_pk = self.kwargs["post_pk"]
        queryset = Image.objects.filter(post__pk=post_pk)
        image_pk = self.kwargs.get("id")
        if image_pk:
            queryset = queryset.filter(id=image_pk)

        return queryset

    def create(self, request, *args, **kwargs):
        post_pk = kwargs.get("post_pk")
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.validated_data["post_id"] = post_pk
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(deprecated=True)
    def update(self, request: Request, *args, **kwargs):
        return Response(
            data={"detail": "Update operation is not supported"},
            status=status.HTTP_404_NOT_FOUND,
        )

    @extend_schema(deprecated=True)
    def partial_update(self, request: Request, *args, **kwargs):
        return Response(
            data={"detail": "Partial Update operation is not supported"},
            status=status.HTTP_404_NOT_FOUND,
        )


@extend_schema(tags=["01. Others"])
class OtherImageListView(APIView):
    serializer_class = ImageSerializer

    def get(self, request):
        user: User = request.user
        images = Image.objects.exclude(author=user)

        serializer = self.serializer_class(images, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["01. My"])
class MyImageListView(APIView):
    serializer_class = ImageSerializer

    def get(self, request):
        user: User = request.user
        images = user.images.all()

        serializer = self.serializer_class(images, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["01. My"])
class LikePostView(APIView):
    def post(self, request, post_id):
        user = request.user

        target = get_object_or_404(Post, pk=post_id)

        like, created = Like.objects.get_or_create(
            content_type=ContentType.objects.get_for_model(target),
            object_id=post_id,
            user=user,
        )

        if not created:
            like.delete()
            return Response(
                data={"detail": "Like Post removed"}, status=status.HTTP_204_NO_CONTENT
            )

        return Response(
            data={"detail": "Like Post added"}, status=status.HTTP_201_CREATED
        )


@extend_schema(tags=["01. My"])
class LikeCommentView(APIView):
    def post(self, request, comment_id):
        user = request.user

        target = get_object_or_404(Comment, pk=comment_id)

        like, created = Like.objects.get_or_create(
            content_type=ContentType.objects.get_for_model(target),
            object_id=comment_id,
            user=user,
        )

        if not created:
            like.delete()
            return Response(
                data={"detail": "Like Comment removed"},
                status=status.HTTP_204_NO_CONTENT,
            )

        return Response(
            data={"detail": "Like Comment added"}, status=status.HTTP_201_CREATED
        )


@extend_schema(tags=["01. My"])
class MyLikePostListView(APIView):
    serializer_class = PostSerializer

    def get(self, request):
        content_type = ContentType.objects.get_for_model(Post)
        liked_posts_id = Like.objects.filter(
            user=request.user, content_type=content_type
        ).values_list("object_id", flat=True)
        liked_posts = Post.objects.filter(id__in=liked_posts_id)

        serializer = self.serializer_class(liked_posts, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["01. My"])
class MyLikeCommentListView(APIView):
    serializer_class = CommentSerializer

    def get(self, request):
        content_type = ContentType.objects.get_for_model(Comment)
        liked_comments_id = Like.objects.filter(
            user=request.user, content_type=content_type
        ).values_list("object_id", flat=True)
        liked_comments = Comment.objects.filter(id__in=liked_comments_id)

        serializer = self.serializer_class(liked_comments, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)
