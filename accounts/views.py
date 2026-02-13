from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import serializers


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
# PROFILE (GET / PUT / PATCH)
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

    def put(self, request):
        """
        Full update (must send all fields)
        """
        profile = request.user.profile

        request.user.username = request.data.get("username", request.user.username)
        request.user.email = request.data.get("email", request.user.email)
        profile.bio = request.data.get("bio", profile.bio)

        request.user.save()
        profile.save()

        return Response({
            "username": request.user.username,
            "email": request.user.email,
            "bio": profile.bio,
            "is_verified": profile.is_verified,
        })

    def patch(self, request):
        """
        Partial update (only send fields you want to change)
        """
        profile = request.user.profile

        if "username" in request.data:
            request.user.username = request.data["username"]

        if "email" in request.data:
            request.user.email = request.data["email"]

        if "bio" in request.data:
            profile.bio = request.data["bio"]

        request.user.save()
        profile.save()

        return Response({
            "username": request.user.username,
            "email": request.user.email,
            "bio": profile.bio,
            "is_verified": profile.is_verified,
        })

