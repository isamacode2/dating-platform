from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import serializers
from .models import Profile, Like, Match


# REGISTER
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


# PROFILE
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


# DISCOVER USERS
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


# LIKE USER
class LikeUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, username):
        try:
            receiver = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        if receiver == request.user:
            return Response({"error": "You cannot like yourself"}, status=400)

        Like.objects.get_or_create(sender=request.user, receiver=receiver)

        # Check if mutual like exists
        if Like.objects.filter(sender=receiver, receiver=request.user).exists():
            Match.objects.get_or_create(user1=request.user, user2=receiver)
            return Response({"match": True})

        return Response({"match": False})


# GET MATCHES
class MatchesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        matches = Match.objects.filter(user1=request.user) | Match.objects.filter(user2=request.user)

        data = []
        for match in matches:
            other_user = match.user2 if match.user1 == request.user else match.user1
            data.append({
                "username": other_user.username
            })

        return Response(data)

