from rest_framework import serializers

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
            "is_admin",
            "created_at",
            "updated_at",
        )
        extra_kwargs = {
            "password": {"write_only": True},
            "fullname": {"required": False},
            "phone": {"required": False},
        }
        read_only_fields = (
            "email",
            "created_at",
            "updated_at",
        )

    def update(self, instance, validated_data):
        if "password" in validated_data:
            new_password = validated_data.pop("password")
            instance.set_password(new_password)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class UserProfileSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, write_only=True)

    user = UserSerializer(label="유저", read_only=True)

    class Meta:
        model = Profile
        fields = (
            "id",
            "user",
            "nickname",
            "birthday",
            "image",
            "image_url",
            "is_public",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "image_url",
            "created_at",
            "updated_at",
        )
        extra_kwargs = {"user": {"write_only": True}}

    def create(self, validated_data):
        validated_data = image_s3_upload(validated_data, "profile")
        validated_data["user"] = self.context.get("user")
        instance = super().create(validated_data)

        return instance

    def update(self, instance, validated_data):
        validated_data = image_s3_upload(validated_data, "profile")
        instance = super().update(instance, validated_data)

        return instance


class ProfileSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, write_only=True)

    class Meta:
        model = Profile
        fields = (
            "id",
            "nickname",
            "birthday",
            "image",
            "image_url",
            "is_public",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "image_url",
            "created_at",
            "updated_at",
        )

    def create(self, validated_data):
        validated_data = image_s3_upload(validated_data, "profile")
        validated_data["user"] = self.context.get("request").user
        instance = super().create(validated_data)

        return instance

    def update(self, instance, validated_data):
        validated_data = image_s3_upload(validated_data, "profile")
        instance = super().update(instance, validated_data)

        return instance


class UserInfoSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(label="프로필", read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "fullname",
            "phone",
            "password",
            "profile",
            "is_active",
            "is_admin",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "email",
            "created_at",
            "updated_at",
        )
        extra_kwargs = {
            "password": {"write_only": True, "required": True},
            "fullname": {"required": False},
            "phone": {"required": False},
        }


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = "__all__"
        read_only_fields = ("created_at",)
