from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import RegisterSerializer, ProfileSerializer
from .models import Profile
from rest_framework.permissions import AllowAny, IsAuthenticated


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class ProfileView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

