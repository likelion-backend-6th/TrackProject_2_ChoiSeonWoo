from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.request import Request
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema
from common.permissions import IsAdminOrReadOnly

from posts.models import Post
from posts.serializers import PostSerializer
from posts.filters import PostFilter
from users.models import User


@extend_schema(tags=["Post"])
class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filterset_class = PostFilter

    def list(self, request: Request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["My"])
class PostInfoView(APIView):
    serializer_class = PostSerializer

    def get(self, request):
        posts = Post.objects.exclude(author=request.user)

        serializer = self.serializer_class(posts, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["My"])
class MyPostView(APIView):
    serializer_class = PostSerializer

    def get(self, request):
        user: User = request.user
        posts = user.posts.all()

        serializer = self.serializer_class(posts, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        post = get_object_or_404(Post, author=request.user, id=id)
        serializer = self.serializer_class(post, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
