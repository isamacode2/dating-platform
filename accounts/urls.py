from django.urls import path
from .views import (
    RegisterView,
    ProfileView,
    FollowUserView,
    UnfollowUserView,
)

urlpatterns = [
    path("", RegisterView.as_view(), name="register"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("follow/<str:username>/", FollowUserView.as_view(), name="follow-user"),
    path("unfollow/<str:username>/", UnfollowUserView.as_view(), name="unfollow-user"),
]

