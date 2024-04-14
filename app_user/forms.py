from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from app_user.models import Profile


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]


class UserDetailsForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()

    phone = forms.CharField(max_length=15)
    birth_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    gender = forms.ChoiceField(choices=Profile.GENDER_CHOICES)
    address = forms.CharField(max_length=200)
    profile_picture = forms.ImageField(
        help_text="Image should be square shaped or in 1:1 ratio."
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
