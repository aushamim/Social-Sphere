from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.views.generic import CreateView, View
from django.views.generic.edit import UpdateView
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from app_user.forms import SignUpForm, UserDetailsForm
from app_user.models import Profile


# Create your views here.
class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = "user_creation_form.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        profile = Profile(user=user)
        profile.save()

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        activation_link = f"http://127.0.0.1:8000/user/activate/{uid}/{token}/"

        message = render_to_string(
            "activate_account.html",
            {
                "activation_link": activation_link,
            },
        )
        subject = "Activate Account"
        email_to = user.email
        send_email = EmailMultiAlternatives(subject, "", to=[email_to])
        send_email.attach_alternative(message, "text/html")
        send_email.send()

        messages.success(
            self.request, "Please check your email to activate your account."
        )

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create an account"
        return context


def activate_acc(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User.objects.get(pk=uid)
    except User.DoesNotExist:
        user = None

    # if user is not None and default_token_generator.check_token(user, token):
    if user is not None:
        user.is_active = True
        user.save()
        messages.success(request, "Account verification successful. Please login.")
        return redirect("login")
    else:
        messages.error(request, "Account verification failed.")
        return redirect("home")


class Login(LoginView):
    template_name = "user_creation_form.html"

    def get_success_url(self):
        return reverse_lazy("home")

    def form_valid(self, form):
        messages.success(self.request, "Logged In Successfully")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Please Login"
        return context


class Logout(View):

    def get(self, request):
        logout(request)
        messages.success(self.request, "Logged Out Successfully")
        return redirect("home")


class EditUserProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserDetailsForm
    template_name = "user_creation_form.html"
    success_url = reverse_lazy("home")

    def get_object(self, queryset=None):
        return self.request.user

    def get_initial(self):
        initial = super().get_initial()
        if self.request.user.is_authenticated:
            user = self.request.user
            profile = Profile.objects.get(user=user)

            initial["phone"] = profile.phone
            initial["birth_date"] = profile.birth_date
            initial["gender"] = profile.gender
            initial["address"] = profile.address
        return initial

    def form_valid(self, form):
        user = form.save(commit=False)
        user.first_name = form.cleaned_data["first_name"]
        user.last_name = form.cleaned_data["last_name"]
        user.email = form.cleaned_data["email"]

        profile = Profile.objects.get(user=user)
        profile.phone = form.cleaned_data["phone"]
        profile.birth_date = form.cleaned_data["birth_date"]
        profile.gender = form.cleaned_data["gender"]
        profile.address = form.cleaned_data["address"]
        profile.profile_picture = form.cleaned_data["profile_picture"]

        user.save()
        profile.save()

        messages.success(self.request, "Successfully updated user information")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Edit User Information"
        return context


def UserProfileView(request, id):
    profile = Profile.objects.get(id=id)
    return render(
        request,
        "user_profile.html",
        {"title": f"{profile.user.username}'s Profile", "profile": profile},
    )
