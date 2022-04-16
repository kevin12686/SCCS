from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserCreationForm
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class LoginForm(AuthenticationForm):

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request=None, *args, **kwargs)
        self.error_messages['username_incorrect'] = _('Username is incorrect.')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 5:
            raise ValidationError(
                self.error_messages['username_incorrect'],
                code='username_incorrect'
            )
        return username


class ResetPasswordForm(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        del self.fields['new_password2']

    def clean_new_password1(self):
        password = self.cleaned_data.get('new_password1')
        password_validation.validate_password(password, self.user)
