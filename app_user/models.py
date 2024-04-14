from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    GENDER_CHOICES = (
        ("Male", "Male"),
        ("Female", "Female"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=6, choices=GENDER_CHOICES, null=True, blank=True
    )
    address = models.CharField(max_length=200, null=True, blank=True)
    profile_picture = models.ImageField(upload_to="profile/", null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.user.username}'s profile"
