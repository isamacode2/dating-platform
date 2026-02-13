from django.urls import path
from .views import RegisterView, ProfileView, UserListView, LikeUserView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("users/", UserListView.as_view(), name="user_list"),
    path("like/<int:user_id>/", LikeUserView.as_view(), name="like_user"),
]

