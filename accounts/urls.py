from django.urls import path
from .views import RegisterView, ProfileView, DiscoverUsersView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("users/", DiscoverUsersView.as_view(), name="discover_users"),
]

