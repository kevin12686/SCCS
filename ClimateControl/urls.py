from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .forms import LoginForm

urlpatterns = [
    path('login/', LoginView.as_view(form_class=LoginForm, template_name='login.html'), name='Login'),
    path('logout/', LogoutView.as_view(), name='Logout'),
]
