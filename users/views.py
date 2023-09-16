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

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema

from common.permissions import IsAdminOrReadOnly
from posts.filters import PostFilter

from posts.models import Post
from posts.serializers import PostSerializer

from users.models import Follow, Profile, User
from users.serializers import (
    UserProfileSerializer,
    ProfileSerializer,
    SignUpSeiralizer,
    LoginSeiralizer,
    UserInfoSerializer,
    UserSerializer,
    FollowSerializer,
)
from users.filters import UserFilter, ProfileFilter, FollowFilter


@extend_schema(tags=["00. Auth"])
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


@extend_schema(tags=["00. Auth"])
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


@extend_schema(tags=["00. Auth"])
class TokenObtainPairView_(TokenObtainPairView):
    pass


@extend_schema(tags=["00. Auth"])
class TokenRefreshView_(TokenRefreshView):
    pass


@extend_schema(tags=["02. User"])
class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filterset_class = UserFilter

    def list(self, request: Request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @extend_schema(deprecated=True)
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

    @action(detail=True, methods=["get"], url_path="feed")
    def feed(self, request: Request, *args, **kwargs):
        user: User = self.get_object()
        following = user.following.all()
        posts = Post.objects.filter(author__in=following)

        serializer = PostSerializer(posts, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["03. Profile"])
class ProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Profile.objects.all()
    serializer_class = UserProfileSerializer
    filterset_class = ProfileFilter

    def list(self, request: Request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["04. Follow"])
class FollowViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    filterset_class = FollowFilter

    def list(self, request: Request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def create(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            qs = Follow.objects.filter(**validated_data)
            if qs.exists():
                qs.delete()
                return Response(
                    data={"message": "Unfollowed successfully"},
                    status=status.HTTP_204_NO_CONTENT,
                )

            serializer.save()
            return Response(
                data={"message": "Followed successfully"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["01. My - User"])
class MyInfoView(APIView):
    serializer_class = UserInfoSerializer

    def get(self, request):
        user: User = request.user

        serializer = self.serializer_class(user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        serializer = self.serializer_class(request.user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["01. My - User"])
class OtherUserInfoView(APIView):
    serializer_class = UserInfoSerializer

    def get(self, request):
        users: User = User.objects.select_related("profile").exclude(id=request.user.id)

        serializer = self.serializer_class(users, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["01. My - Profile"])
class ProfileView(APIView):
    serializer_class = ProfileSerializer

    def get(self, request):
        user: User = request.user
        profile = user.profile

        serializer = self.serializer_class(profile)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        serializer = self.serializer_class(request.user.profile, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["01. My - Profile"])
class OtherProfileView(APIView):
    serializer_class = ProfileSerializer
    filter_backends = DjangoFilterBackend
    filterset_class = ProfileFilter

    def get(self, request):
        profile: Profile = Profile.objects.exclude(user=request.user)
        queryset = self.filter_backends().filter_queryset(request, profile, self)

        serializer = self.serializer_class(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["01. My - Follow"])
class FollowView(APIView):
    serializer_class = FollowSerializer

    def post(self, request, id):
        user: User = request.user

        followee = get_object_or_404(User, id=id)
        follow, created = Follow.objects.get_or_create(user_from=user, user_to=followee)

        if created:
            return Response(
                data={"message": "Followed successfully"},
                status=status.HTTP_201_CREATED,
            )

        follow.delete()

        return Response(
            data={"message": "Unfollowed successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


@extend_schema(tags=["01. My - Follow"])
class FollowingView(APIView):
    serializer_class = UserSerializer
    filter_backends = DjangoFilterBackend
    filterset_class = UserFilter

    def get(self, request):
        user: User = request.user
        following = user.following.all()
        queryset = self.filter_backends().filter_queryset(request, following, self)

        serializer = self.serializer_class(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["01. My - Follow"])
class FollowerView(APIView):
    serializer_class = UserSerializer
    filter_backends = DjangoFilterBackend
    filterset_class = UserFilter

    def get(self, request):
        user: User = request.user
        follower = user.follower.all()
        queryset = self.filter_backends().filter_queryset(request, follower, self)

        serializer = self.serializer_class(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["01. My - Post"])
class FeedView(APIView):
    serializer_class = PostSerializer
    filter_backends = DjangoFilterBackend
    filterset_class = PostFilter

    def get(self, request):
        user = request.user
        following = user.following.all()
        posts = Post.objects.filter(author__in=following)
        queryset = self.filter_backends().filter_queryset(request, posts, self)

        serializer = self.serializer_class(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
