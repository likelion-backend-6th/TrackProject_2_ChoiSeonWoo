from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.request import Request

from drf_spectacular.utils import extend_schema

from posts.models import Post
from posts.permissions import PostCustomReadOnly
from posts.serializers import PostSerializer
from posts.filters import PostFilter


@extend_schema(tags=["Post"])
class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [PostCustomReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filterset_class = PostFilter

    def list(self, request: Request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
