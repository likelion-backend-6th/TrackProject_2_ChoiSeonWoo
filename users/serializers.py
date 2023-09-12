from rest_framework import serializers

from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes

from users.models import Follow, User, Profile
from common.utils import image_s3_upload


class SignUpSeiralizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "fullname",
            "phone",
            "password",
            "created_at",
        )

    def create(self, validated_data):
        email = validated_data["email"]
        fullname = validated_data["fullname"]
        phone = validated_data["phone"]
        password = validated_data["password"]

        user = User.objects.create(email=email, fullname=fullname, phone=phone)
        user.set_password(password)
        user.save()

        return user


class LoginSeiralizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "fullname", "password")
        extra_kwargs = {"password": {"write_only": True}}
        read_only_fields = ("fullname",)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "fullname",
            "password",
            "phone",
            "is_active",
        )
        extra_kwargs = {"password": {"write_only": True}}
        read_only_fields = ("email",)

    def update(self, instance, validated_data):
        if "password" in validated_data:
            new_password = validated_data.pop("password")
            instance.set_password(new_password)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class ProfileUploadSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)

    class Meta:
        model = Profile
        fields = (
            "user",
            "nickname",
            "birthday",
            "image",
            "image_url",
        )
        extra_kwargs = {"image": {"write_only": True}}
        read_only_fields = ("image_url",)

    def create(self, validated_data):
        validated_data = image_s3_upload(validated_data)
        instance = super().create(validated_data)

        return instance

    def update(self, instance, validated_data):
        validated_data = image_s3_upload(validated_data)
        instance = super().update(instance, validated_data)

        return instance


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_user(self, obj: Profile):
        user = obj.user
        return UserSerializer(user).data

    class Meta:
        model = Profile
        fields = (
            "id",
            "user",
            "nickname",
            "birthday",
            "image_url",
            "is_public",
            "is_active",
        )


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        exclude = ("created_at",)
