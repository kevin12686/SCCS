from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class LoginForm(AuthenticationForm):
    pass

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 5:
            raise ValidationError(
                _('Username is not correct.'),
                code='username_incorrect'
            )
        return username
