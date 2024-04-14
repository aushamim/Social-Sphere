from django.urls import path

from app_dashboard.views import CreatePostView, MyPosts

urlpatterns = [
    path("add-post/", CreatePostView.as_view(), name="add-post"),
    path("my-posts/", MyPosts, name="my-posts"),
]
