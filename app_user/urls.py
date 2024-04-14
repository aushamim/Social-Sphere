from django.urls import include, path

from app_user.views import (
    EditUserProfileView,
    Login,
    Logout,
    SignUpView,
    UserProfileView,
    activate_acc,
)

urlpatterns = [
    path("sign-up/", SignUpView.as_view(), name="sign-up"),
    path("login/", Login.as_view(), name="login"),
    path("logout/", Logout.as_view(), name="logout"),
    path("activate/<uid64>/<token>/", activate_acc, name="activate"),
    path("profile/<int:id>", UserProfileView, name="profile"),
    path("edit/", EditUserProfileView.as_view(), name="edit-user"),
]
