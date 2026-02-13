from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import serializers
from .models import Profile


# =========================
# REGISTER
# =========================

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email"),
            password=validated_data["password"],
        )


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    authentication_classes = []


# =========================
# PROFILE
# =========================

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = request.user.profile
        return Response({
            "username": request.user.username,
            "email": request.user.email,
            "bio": profile.bio,
            "is_verified": profile.is_verified,
        })

    def patch(self, request):
        profile = request.user.profile

        if "bio" in request.data:
            profile.bio = request.data["bio"]

        profile.save()

        return Response({
            "username": request.user.username,
            "email": request.user.email,
            "bio": profile.bio,
            "is_verified": profile.is_verified,
        })


# =========================
# DISCOVER USERS
# =========================

class DiscoverUsersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = Profile.objects.exclude(user=request.user)

        data = []
        for profile in users:
            data.append({
                "username": profile.user.username,
                "bio": profile.bio,
                "is_verified": profile.is_verified,
            })

        return Response(data)

