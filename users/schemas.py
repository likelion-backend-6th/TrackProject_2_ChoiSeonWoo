from drf_spectacular.utils import OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from posts.serializers import CommentSerializer, PostSerializer


SIGN_UP = {"operation_id": "회원가입 【공용】"}
LOGIN = {"operation_id": "로그인 【공용】"}
CREATE_TOKEN = {"operation_id": "토큰 발급 【공용】"}
REFRESH_TOKEN = {"operation_id": "토큰 갱신 【공용】"}

USER_LIST = {
    "operation_id": "유저 목록 조회 【유저 전용】",
    "parameters": [
        OpenApiParameter(
            name="email",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="【입력값 포함 검색】 유저의 이메일 주소",
        ),
        OpenApiParameter(
            name="fullname",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="【입력값 포함 검색】 유저의 이름",
        ),
        OpenApiParameter(
            name="phone",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="【입력값 포함 검색】 유저의 휴대폰번호",
        ),
        OpenApiParameter(
            name="is_active",
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY,
            description="【관리자 전용】 유저의 계정 활성화 여부",
        ),
    ],
}
USER_CREATE = {"operation_id": "유저 생성 【미사용】"}
USER_RETRIEVE = {
    "operation_id": "유저 조회 【유저 전용】",
    "parameters": [
        OpenApiParameter(
            name="id",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description="유저의 ID",
        ),
    ],
}
USER_UPDATE = {
    "operation_id": "유저 수정 【관리자 전용】",
    "parameters": [
        OpenApiParameter(
            name="id",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description="유저의 ID",
        ),
    ],
}
USER_PARTIAL_UPDATE = {
    "operation_id": "유저 일부 수정【관리자 전용】",
    "parameters": [
        OpenApiParameter(
            name="id",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description="유저의 ID",
        ),
    ],
}
USER_DESTROY = {
    "operation_id": "유저 삭제 【관리자 전용】",
    "parameters": [
        OpenApiParameter(
            name="id",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description="유저의 ID",
        ),
    ],
}
USER_FOLLOW = {
    "operation_id": "팔로우 생성/해제 【유저 전용】",
    "request": None,
    "responses": {
        201: OpenApiTypes.OBJECT,
        204: OpenApiTypes.OBJECT,
    },
    "parameters": [
        OpenApiParameter(
            name="id",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.PATH,
            description="팔로우 신청 유저 ID",
        ),
        OpenApiParameter(
            name="user_id",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.PATH,
            description="팔로우 받을 유저 ID",
        ),
    ],
    "examples": [
        OpenApiExample(
            name="follow_success_example",
            response_only=True,
            status_codes=["201"],
            value=[{"detail": "Follow successfully"}],
        ),
        OpenApiExample(
            name="unfollow_success_example",
            response_only=True,
            status_codes=["204"],
            value={"detail": "Unfollowed successfully"},
        ),
    ],
}
USER_FOLLOWING = {
    "operation_id": "유저의 팔로잉 조회 【유저 전용】",
    "parameters": [
        OpenApiParameter(
            name="id",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description="유저의 ID",
        ),
    ],
}
USER_FOLLOWER = {
    "operation_id": "유저의 팔로워 조회 【유저 전용】",
    "parameters": [
        OpenApiParameter(
            name="id",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description="유저의 ID",
        ),
    ],
}
USER_POSTS = {
    "operation_id": "유저의 게시글 모아보기 【유저 전용】",
    "responses": {
        200: PostSerializer,
    },
    "parameters": [
        OpenApiParameter(
            name="id",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description="유저의 ID",
        ),
    ],
}
USER_FEED = {
    "operation_id": "유저의 피드 조회 【유저 전용】",
    "responses": {
        200: PostSerializer,
    },
    "parameters": [
        OpenApiParameter(
            name="id",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description="유저의 ID",
        ),
    ],
}
USER_COMMENTS = {
    "operation_id": "유저의 댓글 모아보기 【유저 전용】",
    "responses": {
        200: CommentSerializer,
    },
    "parameters": [
        OpenApiParameter(
            name="id",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description="유저의 ID",
        ),
    ],
}

PROFILE_GET = {
    "operation_id": "프로필 보기 【유저 전용】",
    "parameters": [
        OpenApiParameter(
            name="user_pk",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description="유저의 ID",
        ),
    ],
}
PROFILE_POST = {
    "operation_id": "프로필 생성 【관리자 전용】",
    "parameters": [
        OpenApiParameter(
            name="user_pk",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description="유저의 ID",
        ),
    ],
}
PROFILE_PUT = {
    "operation_id": "프로필 수정 【관리자 전용】",
    "parameters": [
        OpenApiParameter(
            name="user_pk",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description="유저의 ID",
        ),
    ],
}
PROFILE_DELETE = {
    "operation_id": "프로필 삭제 【관리자 전용】",
    "parameters": [
        OpenApiParameter(
            name="user_pk",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description="유저의 ID",
        ),
    ],
}

FOLLOW_LIST = {
    "operation_id": "팔로우 목록 조회 【유저 전용】",
    "examples": [
        OpenApiExample(
            name="success_example",
            response_only=True,
            value=[
                {
                    "id": 0,
                    "created_at": "2023-09-18T13:01:03.304Z",
                    "user_from": 0,
                    "user_to": 0,
                }
            ],
        )
    ],
    "parameters": [
        OpenApiParameter(
            name="user_from",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description="【일치값 검색】팔로워(팔로우 신청 유저)의 ID",
        ),
        OpenApiParameter(
            name="user_to",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description="【일치값 검색】팔로잉(팔로우 받은 유저)의 ID",
        ),
    ],
}

MY_INFO_GET = {
    "operation_id": "내 정보 조회 【유저 전용】",
}
MY_INFO_PATCH = {
    "operation_id": "내 정보 수정 【유저 전용】",
}

OTHERS_INFO = {
    "operation_id": "다른 유저 목록 조회 【유저 전용】",
    "parameters": [
        OpenApiParameter(
            name="email",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="【입력값 포함 검색】 유저의 이메일 주소",
        ),
        OpenApiParameter(
            name="fullname",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="【입력값 포함 검색】 유저의 이름",
        ),
        OpenApiParameter(
            name="phone",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="【입력값 포함 검색】 유저의 휴대폰번호",
        ),
    ],
}

MY_PROFILE_GET = {"operation_id": "내 프로필 보기 【유저 전용】"}
MY_PROFILE_POST = {"operation_id": "내 프로필 생성 【유저 전용】"}
MY_PROFILE_PATCH = {"operation_id": "내 프로필 수정 【유저 전용】"}

OTHERS_PROFILE = {
    "operation_id": "다른 유저 프로필 목록 조회 【유저 전용】",
    "parameters": [
        OpenApiParameter(
            name="nickname",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="【입력값 포함 검색】 프로필 닉네임",
        ),
        OpenApiParameter(
            name="is_active",
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY,
            description="【관리자 전용】 프로필 활성화 여부",
        ),
    ],
}

MY_FOLLOW = {
    "operation_id": "나의 팔로우 생성/해제 【유저 전용】",
    "parameters": [
        OpenApiParameter(
            name="user_id",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description="내가 팔로우 신청할 유저의 ID",
        ),
    ],
}
MY_FOLLOWING = {
    "operation_id": "나의 팔로잉 조회 【유저 전용】",
    "parameters": [
        OpenApiParameter(
            name="email",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="【입력값 포함 검색】 유저의 이메일 주소",
        ),
        OpenApiParameter(
            name="fullname",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="【입력값 포함 검색】 유저의 이름",
        ),
        OpenApiParameter(
            name="phone",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="【입력값 포함 검색】 유저의 휴대폰번호",
        ),
    ],
}
MY_FOLLOWER = {
    "operation_id": "나의 팔로워 조회 【유저 전용】",
    "parameters": [
        OpenApiParameter(
            name="email",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="【입력값 포함 검색】 유저의 이메일 주소",
        ),
        OpenApiParameter(
            name="fullname",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="【입력값 포함 검색】 유저의 이름",
        ),
        OpenApiParameter(
            name="phone",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="【입력값 포함 검색】 유저의 휴대폰번호",
        ),
    ],
}
