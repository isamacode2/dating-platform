from django.urls import path
from .views import (
    RegisterView,
    ProfileView,
    DiscoverUsersView,
    LikeUserView,
    MatchesView
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("users/", DiscoverUsersView.as_view(), name="discover_users"),
    path("like/<str:username>/", LikeUserView.as_view(), name="like_user"),
    path("matches/", MatchesView.as_view(), name="matches"),
]

