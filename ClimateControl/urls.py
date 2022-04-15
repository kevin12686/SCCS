from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import ResetPasswordView, IndexView, UserListView, UserUpdateView, UserCreateView, UserDeleteView
from .forms import LoginForm

urlpatterns = [
    path('', IndexView.as_view(), name='Index'),
    path('login/', LoginView.as_view(form_class=LoginForm, template_name='login.html'), name='Login'),
    path('logout/', LogoutView.as_view(), name='Logout'),
    path('reset/', ResetPasswordView.as_view(template_name='password_reset.html'), name='PasswordReset'),
    path('user/', UserListView.as_view(), name='UserList'),
    path('user/create/', UserCreateView.as_view(), name='UserCreate'),
    path('user/update/<pk>/', UserUpdateView.as_view(), name='UserUpdate'),
    path('user/delete/<pk>/', UserDeleteView.as_view(), name='UserDelete')
]
