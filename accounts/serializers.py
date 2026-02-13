from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile, Follow


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user


class ProfilePrivateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Profile
        fields = (
            "username",
            "email",
            "display_name",
            "bio",
            "location",
            "role",
            "bio_visibility",
            "location_visibility",
            "role_visibility",
            "is_verified",
            "verification_level",
            "created_at",
        )


class FollowSerializer(serializers.ModelSerializer):
    follower = serializers.CharField(source="follower.username", read_only=True)
    following = serializers.CharField(source="following.username", read_only=True)

    class Meta:
        model = Follow
        fields = ("follower", "following", "is_approved", "created_at")

