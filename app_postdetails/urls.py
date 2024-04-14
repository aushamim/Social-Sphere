from django.urls import path

from app_postdetails.views import (
    CommentEditView,
    DeleteCommentView,
    DeletePostView,
    LikePostView,
    LikePostViewHome,
    PostDetailView,
    PostEditView,
    UnLikePostView,
    UnLikePostViewHome,
)

urlpatterns = [
    path("details/<int:id>/", PostDetailView.as_view(), name="post-details"),
    path("delete/<int:id>/", DeletePostView.as_view(), name="delete-post"),
    path(
        "details/<int:id>/comment/edit/<int:comment_id>/",
        CommentEditView.as_view(),
        name="edit-comment",
    ),
    path(
        "details/<int:id>/comment/delete/<int:comment_id>/",
        DeleteCommentView.as_view(),
        name="delete-comment",
    ),
    path("edit/<int:id>/", PostEditView.as_view(), name="edit-post"),
    path("like/<int:id>/", LikePostView.as_view(), name="like-post"),
    path("unlike/<int:id>/", UnLikePostView.as_view(), name="unlike-post"),
    path("like-h/<int:id>/", LikePostViewHome.as_view(), name="like-post-h"),
    path("unlike-h/<int:id>/", UnLikePostViewHome.as_view(), name="unlike-post-h"),
]
