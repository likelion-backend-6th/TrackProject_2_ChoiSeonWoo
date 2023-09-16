from rest_framework import serializers

from taggit.serializers import TagListSerializerField

from posts.models import Comment, Post
from users.models import User


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ("post",)


class PostSerializer(serializers.ModelSerializer):
    tags = TagListSerializerField(required=False)
    comments = serializers.SerializerMethodField()

    def get_comments(self, obj: Comment):
        try:
            comments = obj.comments
            return CommentSerializer(comments, many=True).data
        except Comment.DoesNotExist:
            return None

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "author",
            "body",
            "comments",
            "status",
            "is_active",
            "publish",
            "tags",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "publish",
            "created_at",
            "updated_at",
        )

    def create(self, validated_data):
        tags_data = validated_data.pop("tags", [])
        instance = self.Meta.model.objects.create(**validated_data)
        instance.tags.add(*tags_data)

        return instance

    def update(self, instance, validated_data):
        tags_data = validated_data.pop("tags", [])
        instance = super().update(instance, validated_data)
        instance.tags.add(*tags_data)

        return instance
