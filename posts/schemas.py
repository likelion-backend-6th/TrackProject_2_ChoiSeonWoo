from drf_spectacular.utils import OpenApiParameter
from drf_spectacular.types import OpenApiTypes


POST_LIST = {
    "operation_id": "게시글 목록 조회 【유저 전용】",
    "parameters": [
        OpenApiParameter(
            name="title",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="【입력값 포함 검색】 게시글 제목",
        ),
        OpenApiParameter(
            name="nickname",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="【입력값 포함 검색】 게시글 작성자 닉네임",
        ),
        OpenApiParameter(
            name="body",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="【입력값 포함 검색】 게시글 본문",
        ),
        OpenApiParameter(
            name="tags",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="【일치값 검색】 게시글의 태그(콤마로 구분하여 여러값 입력 가능)",
        ),
        OpenApiParameter(
            name="status",
            type=OpenApiTypes.INT,
            enum=[0, 1],
            location=OpenApiParameter.QUERY,
            description="【관리자 전용】 게시 상태(0: 임시 저장, 1: 게시됨)",
        ),
        OpenApiParameter(
            name="is_active",
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY,
            description="【관리자 전용】 게시글 활성화 여부",
        ),
    ],
}
POST_CREATE = {"operation_id": "게시글 생성 【관리자 전용】"}
POST_RETRIEVE = {
    "operation_id": "게시글 조회 【유저 전용】",
    "parameters": [
        OpenApiParameter(
            name="id",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description="게시글의 ID",
        ),
    ],
}
POST_UPDATE = {
    "operation_id": "게시글 수정 【관리자 전용】",
    "parameters": [
        OpenApiParameter(
            name="id",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description="게시글의 ID",
        ),
    ],
}
POST_PARTIAL_UPDATE = {
    "operation_id": "게시글 일부 수정 【유저 전용】",
    "parameters": [
        OpenApiParameter(
            name="id",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description="게시글의 ID",
        ),
    ],
}
POST_DESTROY = {
    "operation_id": "게시글 삭제 【관리자 전용】",
    "parameters": [
        OpenApiParameter(
            name="id",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description="게시글의 ID",
        ),
    ],
}

OTHERS_POST_LIST = {
    "operation_id": "타인 게시글 목록 조회 【유저 전용】",
    "parameters": [
        OpenApiParameter(
            name="title",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="【입력값 포함 검색】 게시글 제목",
        ),
        OpenApiParameter(
            name="nickname",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="【입력값 포함 검색】 게시글 작성자 닉네임",
        ),
        OpenApiParameter(
            name="body",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="【입력값 포함 검색】 게시글 본문",
        ),
        OpenApiParameter(
            name="tags",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="【일치값 검색】 게시글의 태그(콤마로 구분하여 여러값 입력 가능)",
        ),
    ],
}
My_POST_LIST = {
    "operation_id": "내 게시글 모아보기 【유저 전용】",
    "parameters": [
        OpenApiParameter(
            name="title",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="【입력값 포함 검색】 게시글 제목",
        ),
        OpenApiParameter(
            name="nickname",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="【입력값 포함 검색】 게시글 작성자 닉네임",
        ),
        OpenApiParameter(
            name="body",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="【입력값 포함 검색】 게시글 본문",
        ),
        OpenApiParameter(
            name="tags",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="【일치값 검색】 게시글의 태그(콤마로 구분하여 여러값 입력 가능)",
        ),
    ],
}
My_FEED_LIST = {
    "operation_id": "내 피드 목록 조회 【유저 전용】",
    "parameters": [
        OpenApiParameter(
            name="title",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="【입력값 포함 검색】 게시글 제목",
        ),
        OpenApiParameter(
            name="nickname",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="【입력값 포함 검색】 게시글 작성자 닉네임",
        ),
        OpenApiParameter(
            name="body",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="【입력값 포함 검색】 게시글 본문",
        ),
        OpenApiParameter(
            name="tags",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="【일치값 검색】 게시글의 태그(콤마로 구분하여 여러값 입력 가능)",
        ),
    ],
}

COMMENT_LIST = {
    "operation_id": "댓글 목록 조회 【유저 전용】",
    "parameters": [
        OpenApiParameter(
            name="post_pk",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description="게시글의 ID",
        ),
        OpenApiParameter(
            name="nickname",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="【입력값 포함 검색】 댓글 작성자 닉네임",
        ),
        OpenApiParameter(
            name="body",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="【입력값 포함 검색】 댓글 본문",
        ),
    ],
}
COMMENT_CREATE = {
    "operation_id": "댓글 생성 【유저 전용】",
    "parameters": [
        OpenApiParameter(
            name="post_pk",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description="게시글의 ID",
        ),
    ],
}
COMMENT_RETRIEVE = {
    "operation_id": "댓글 조회 【유저 전용】",
    "parameters": [
        OpenApiParameter(
            name="post_pk",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description="게시글의 ID",
        ),
        OpenApiParameter(
            name="id",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description="댓글의 ID",
        ),
    ],
}
COMMENT_UPDATE = {
    "operation_id": "댓글 수정 【관리자 전용】",
    "parameters": [
        OpenApiParameter(
            name="post_pk",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description="게시글의 ID",
        ),
        OpenApiParameter(
            name="id",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description="댓글의 ID",
        ),
    ],
}
COMMENT_PARTIAL_UPDATE = {
    "operation_id": "댓글 일부 수정 【유저 전용】",
    "parameters": [
        OpenApiParameter(
            name="post_pk",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description="게시글의 ID",
        ),
        OpenApiParameter(
            name="id",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description="댓글의 ID",
        ),
    ],
}
COMMENT_DESTROY = {
    "operation_id": "댓글 삭제 【관리자 전용】",
    "parameters": [
        OpenApiParameter(
            name="post_pk",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description="게시글의 ID",
        ),
        OpenApiParameter(
            name="id",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description="댓글의 ID",
        ),
    ],
}

My_COMMENT_LIST = {
    "operation_id": "내 댓글 모아보기 【유저 전용】",
    "parameters": [
        OpenApiParameter(
            name="nickname",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="【입력값 포함 검색】 댓글 작성자 닉네임",
        ),
        OpenApiParameter(
            name="body",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="【입력값 포함 검색】 댓글 본문",
        ),
    ],
}


IMAGE_LIST = {
    "operation_id": "이미지 목록 조회 【유저 전용】",
    "parameters": [
        OpenApiParameter(
            name="post_pk",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description="게시글의 ID",
        ),
    ],
}
IMAGE_CREATE = {"operation_id": "이미지 생성 【유저 전용】"}
IMAGE_RETRIEVE = {
    "operation_id": "이미지 조회 【유저 전용】",
    "parameters": [
        OpenApiParameter(
            name="post_pk",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description="게시글의 ID",
        ),
        OpenApiParameter(
            name="id",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description="이미지의 ID",
        ),
    ],
}
IMAGE_UPDATE = {"operation_id": "이미지 수정 【미사용】"}
IMAGE_PARTIAL_UPDATE = {
    "operation_id": "이미지 일부 수정 【미사용】",
}
IMAGE_DESTROY = {
    "operation_id": "이미지 삭제 【관리자 전용】",
    "parameters": [
        OpenApiParameter(
            name="post_pk",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description="게시글의 ID",
        ),
        OpenApiParameter(
            name="id",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description="이미지의 ID",
        ),
    ],
}

OTHERS_IMAGE_LIST = {"operation_id": "타인 이미지 모아보기 【유저 전용】"}
My_IMAGE_LIST = {"operation_id": "내 이미지 모아보기 【유저 전용】"}

LIKE_POST = {
    "operation_id": "나의 게시글 좋아요 생성/취소 조회 【유저 전용】",
    "parameters": [
        OpenApiParameter(
            name="post_id",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description="게시글의 ID",
        ),
    ],
}
LIKE_COMMENT = {
    "operation_id": "나의 댓글 좋아요 생성/취소 조회 【유저 전용】",
    "parameters": [
        OpenApiParameter(
            name="comment_id",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description="댓글의 ID",
        ),
    ],
}

MY_LIKED_POSTS = {
    "operation_id": "내가 좋아요 누른 게시글 모아보기 【유저 전용】",
    "parameters": [
        OpenApiParameter(
            name="title",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="【입력값 포함 검색】 게시글 제목",
        ),
        OpenApiParameter(
            name="nickname",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="【입력값 포함 검색】 게시글 작성자 닉네임",
        ),
        OpenApiParameter(
            name="body",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="【입력값 포함 검색】 게시글 본문",
        ),
        OpenApiParameter(
            name="tags",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="【일치값 검색】 게시글의 태그(콤마로 구분하여 여러값 입력 가능)",
        ),
    ],
}
MY_LIKED_COMMENTS = {"operation_id": "내가 좋아요 누른 댓글 모아보기 【유저 전용】"}
