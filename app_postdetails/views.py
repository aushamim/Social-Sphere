from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, UpdateView, DeleteView
from django.views.generic.base import View
from django.contrib import messages

from app_postdetails.forms import CommentForm, PostEditForm
from app_postdetails.models import Comment, Post


# Create your views here.
class PostDetailView(DetailView):
    model = Post
    pk_url_kwarg = "id"
    template_name = "post_detail.html"

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(data=self.request.POST)
        post = self.get_object()
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.user = self.request.user
            new_comment.post = post
            new_comment.save()
            post.comments.add(new_comment)
        return redirect("post-details", post.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = self.get_object().comments.all().order_by("-timestamp")
        comment_form = CommentForm()

        context["title"] = "Post Details"
        context["comment_form"] = comment_form
        context["comments"] = comments
        return context


class PostEditView(UpdateView):
    model = Post
    form_class = PostEditForm
    pk_url_kwarg = "id"
    template_name = "post_update.html"

    def get_success_url(self):
        messages.success(self.request, "Post uppdated successfully.")
        return reverse("post-details", kwargs={"id": self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Edit Post"
        return context


class LikePostView(View):
    def post(self, request, *args, **kwargs):
        post = Post.objects.get(id=kwargs["id"])
        post.like_post(request.user)
        return redirect("post-details", post.id)


class UnLikePostView(View):
    def post(self, request, *args, **kwargs):
        post = Post.objects.get(id=kwargs["id"])
        post.unlike_post(request.user)
        return redirect("post-details", post.id)


class LikePostViewHome(View):
    def post(self, request, *args, **kwargs):
        post = Post.objects.get(id=kwargs["id"])
        post.like_post(request.user)
        return redirect(f"/#post-{post.id}")


class UnLikePostViewHome(View):
    def post(self, request, *args, **kwargs):
        post = Post.objects.get(id=kwargs["id"])
        post.unlike_post(request.user)
        return redirect(f"/#post-{post.id}")


class CommentEditView(DetailView):
    model = Post
    pk_url_kwarg = "id"
    template_name = "post_detail.html"

    def post(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, id=self.kwargs["comment_id"])
        comment_form = CommentForm(data=self.request.POST, instance=comment)
        post = self.get_object()
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.user = self.request.user
            new_comment.post = post
            new_comment.save()
            post.comments.add(new_comment)
        return redirect("post-details", post.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = self.get_object().comments.all().order_by("-timestamp")
        comment_form = CommentForm()

        comment_id = self.kwargs["comment_id"]
        if comment_id:
            comment = get_object_or_404(Comment, id=comment_id)
            comment_form = CommentForm(instance=comment)

        context["title"] = "Edit Comment"
        context["comment_form"] = comment_form
        context["comments"] = comments
        return context


class DeletePostView(DeleteView):
    model = Post
    template_name = "confirm_post_delete.html"
    success_url = reverse_lazy("home")

    def get_object(self, queryset=None):
        return Post.objects.get(id=self.kwargs["id"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Delete Post"
        return context


class DeleteCommentView(DeleteView):
    model = Comment
    template_name = "confirm_comment_delete.html"

    def get_object(self, queryset=None):
        return Comment.objects.get(id=self.kwargs["comment_id"])

    def get_success_url(self):
        return reverse("post-details", kwargs={"id": self.kwargs["id"]})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Delete Comment"
        return context
