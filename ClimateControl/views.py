from django.shortcuts import render
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, CreateView, TemplateView
from .forms import ResetPasswordForm


# Create your views here.

class ResetPasswordView(PasswordChangeView):
    form_class = ResetPasswordForm
    template_name = 'password_reset.html'

    def get_success_url(self):
        messages.success(self.request, _('Password Changed'))
        return reverse_lazy('Index')


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'


class UserListView(ListView):
    model = get_user_model()
    template_name = 'UserList.html'


class UserCreateView(CreateView):
    model = get_user_model()
    template_name = 'UserFrom.html'
    fields = ['username', 'password', 'is_admin']

    def get_success_url(self):
        messages.success(self.request, _('User created'))
        return reverse_lazy('UserList')
