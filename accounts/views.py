from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Profile
from .serializers import RegisterSerializer, ProfilePrivateSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class ProfileView(generics.RetrieveAPIView):
    serializer_class = ProfilePrivateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

