from django import forms

from app_postdetails.models import Comment, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["post", "image"]


class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["post", "image"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["comment"]


class CommentEditForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["comment"]
