from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.request import Request
from rest_framework.decorators import action


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from drf_spectacular.utils import extend_schema

from posts.models import Post
from posts.serializers import PostSerializer

from users.models import Follow, Profile, User
from users.permissions import UserCustomReadOnly
from users.serializers import (
    FollowSerializer,
    ProfileUploadSerializer,
    ProfileSerializer,
    SignUpSeiralizer,
    LoginSeiralizer,
    UserSerializer,
)
from users.filters import FollowFilter, UserFilter, ProfileFilter


@extend_schema(tags=["Auth"])
class SignUpView(APIView):
    serializer_class = SignUpSeiralizer
    permission_classes = [AllowAny]

    def post(self, request: Request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)

            return Response(
                {
                    "user": serializer.data,
                    "message": "register successs",
                    "token": {"access": access_token, "refresh": refresh_token},
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["Auth"])
class LoginView(APIView):
    serializer_class = LoginSeiralizer
    permission_classes = [AllowAny]

    def post(self, request: Request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(email=email, password=password)

        if user is not None:
            serializer = self.serializer_class(user)
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)

            return Response(
                {
                    "user": serializer.data,
                    "message": "login successs",
                    "token": {"access": access_token, "refresh": refresh_token},
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"message": "login failed"}, status=status.HTTP_401_UNAUTHORIZED
        )


@extend_schema(tags=["Auth"])
class TokenObtainPairView_(TokenObtainPairView):
    pass


@extend_schema(tags=["Auth"])
class TokenRefreshView_(TokenRefreshView):
    pass


@extend_schema(tags=["User"])
class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [UserCustomReadOnly]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filterset_class = UserFilter

    def list(self, request: Request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def create(self, request: Request, *args, **kwargs):
        return Response(
            data={"message": "Create operation is not supported"},
            status=status.HTTP_404_NOT_FOUND,
        )

    @action(detail=True, methods=["get"], url_name="profile")
    def profile(self, request: Request, *args, **kwargs):
        user: User = self.get_object()

        profile = user.profile
        serializer = ProfileSerializer(profile)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["post"],
        url_path=r"follow/(?P<id>[0-9]+)",
    )
    def follow(self, request: Request, pk, id):
        user: User = User.objects.get(id=pk)

        followee = get_object_or_404(User, id=id)
        follow, created = Follow.objects.get_or_create(user_from=user, user_to=followee)

        if created:
            return Response(
                data={"message": "Follow successfully"}, status=status.HTTP_201_CREATED
            )

        follow.delete()

        return Response(
            data={"message": "Unfollowed successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )

    @action(detail=True, methods=["get"], url_name="following")
    def following(self, request: Request, *args, **kwargs):
        user: User = self.get_object()

        following = user.following.all()
        serializer = self.get_serializer(following, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"], url_name="follower")
    def follower(self, request: Request, *args, **kwargs):
        user: User = self.get_object()

        following = user.follower.all()
        serializer = self.get_serializer(following, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"], url_name="posts")
    def posts(self, request: Request, *args, **kwargs):
        user: User = self.get_object()
        posts = user.posts.all()

        serializer = PostSerializer(posts, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"], url_path="following-posts")
    def following_posts(self, request: Request, *args, **kwargs):
        user: User = self.get_object()
        following = user.following.all()
        posts = Post.objects.filter(author__in=following)

        serializer = PostSerializer(posts, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["Profile"])
class ProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [UserCustomReadOnly]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    filterset_class = ProfileFilter

    def get_serializer_class(self):
        if self.action not in ["list", "retrieve"]:
            return ProfileUploadSerializer
        return super().get_serializer_class()

    def list(self, request: Request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["Follow"])
class FollowViewSet(viewsets.ModelViewSet):
    permission_classes = [UserCustomReadOnly]
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    filterset_class = FollowFilter

    def list(self, request: Request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
