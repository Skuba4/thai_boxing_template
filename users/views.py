from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import RegisterUserForm


class RegUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/reg.html'
    success_url = reverse_lazy('users:log')


class Login(LoginView):
    form_class = AuthenticationForm
    template_name = 'users/log.html'
