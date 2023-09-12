from django_filters import rest_framework as filters

from posts.models import Post


class PostFilter(filters.FilterSet):
    title = filters.CharFilter(field_name="title", lookup_expr="icontains")
    nickname = filters.CharFilter(
        field_name="author__profile__nickname", lookup_expr="icontains"
    )
    body = filters.CharFilter(field_name="body", lookup_expr="icontains")
    status = filters.NumberFilter(field_name="status", lookup_expr="exact")
    is_active = filters.BooleanFilter(field_name="is_public", lookup_expr="exact")
    tags = filters.CharFilter(method="filter_by_tags")

    class Meta:
        model = Post
        fields = ["title", "nickname", "body", "status", "is_active", "tags"]

    def filter_by_tags(self, queryset, name, value):
        tags = value.split(",")
        result = queryset

        for tag in tags:
            result = result.filter(tags__name=tag)

        return result
