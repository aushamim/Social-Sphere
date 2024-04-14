from django.shortcuts import render

from app_postdetails.models import Post


# Create your views here.
def Home(request):
    posts = Post.objects.all().order_by("-timestamp")
    return render(request, "home.html", {"posts": posts})
