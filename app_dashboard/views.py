from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic.edit import CreateView

from app_postdetails.forms import PostForm
from app_postdetails.models import Post


class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "create_post.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Successfully uploaded a new post")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create Post"
        return context


@login_required
def MyPosts(request):
    posts = Post.objects.filter(user=request.user)
    return render(request, "my_posts.html", {"title": "My Posts", "posts": posts})
