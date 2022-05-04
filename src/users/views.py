from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse


class LoginView(LoginView):
    template_name = "login.html"

    def get_success_url(self):
        return reverse("library:dashboard")


class LogoutView(LogoutView):
    next_page = "users:login"
