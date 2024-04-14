from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.TextField()
    image = models.ImageField(upload_to="post/", null=True, blank=True)
    likes = models.ManyToManyField(User, blank=True, related_name="liked_users")
    comments = models.ManyToManyField(
        "Comment", blank=True, related_name="all_comments"
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post {self.pk}"

    def like_post(self, user):
        self.likes.add(user)

    def unlike_post(self, user):
        self.likes.remove(user)

    def __str__(self):
        return f"Post by {self.user}"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()

    def __str__(self):
        return f"Comment by {self.user}"
