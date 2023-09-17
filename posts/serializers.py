from rest_framework import serializers

from taggit.serializers import TagListSerializerField

from posts.models import Comment, Image, Post
from users.models import User
from common.utils import image_s3_upload


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ("post",)


class CommentReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ("post",)


class ImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=True, write_only=True)

    class Meta:
        model = Image
        fields = (
            "id",
            "name",
            "post",
            "author",
            "image",
            "image_url",
            "is_active",
            "created_at",
        )
        read_only_fields = (
            "name",
            "post",
            "author",
            "image_url",
            "created_at",
        )

    def create(self, validated_data):
        name = validated_data.get("image").name
        validated_data = image_s3_upload(validated_data, "images")
        validated_data["name"] = name
        validated_data["author"] = self.context.get("request").user

        instance = super().create(validated_data)

        return instance


class ImageReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        exclude = ("post",)


class PostSerializer(serializers.ModelSerializer):
    tags = TagListSerializerField(required=False)
    comments = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    def get_comments(self, obj: Comment):
        try:
            comments = obj.comments
            return CommentReadSerializer(comments, many=True).data
        except Comment.DoesNotExist:
            return None

    def get_images(self, obj: Comment):
        try:
            images = obj.images
            return ImageReadSerializer(images, many=True).data
        except Image.DoesNotExist:
            return None

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "author",
            "body",
            "comments",
            "images",
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
