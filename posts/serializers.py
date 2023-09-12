from rest_framework import serializers

from taggit.serializers import TagListSerializerField, TaggitSerializer

from posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    tags = TagListSerializerField(required=False)

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "author",
            "body",
            "status",
            "is_active",
            "publish",
            "tags",
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
