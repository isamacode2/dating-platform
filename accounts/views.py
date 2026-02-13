from django.contrib.auth.models import User
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializer, UserSerializer
from .models import Like


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class ProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.exclude(id=self.request.user.id)


class LikeUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        try:
            target_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        if target_user == request.user:
            return Response({"error": "Cannot like yourself"}, status=400)

        like, created = Like.objects.get_or_create(
            from_user=request.user,
            to_user=target_user
        )

        if not created:
            return Response({"message": "Already liked"}, status=200)

        # Check if it's a match
        if Like.objects.filter(from_user=target_user, to_user=request.user).exists():
            return Response({"match": True}, status=201)

        return Response({"liked": True}, status=201)

