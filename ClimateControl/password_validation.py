from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
import re


class SymbolIncludeValidator:
    def validate(self, password, user=None):
        if not re.match(r'.*\W.*', password):
            raise ValidationError(
                _("This password must contain at least a symbol."),
                code='password_no_symbol',
            )

    def get_help_text(self):
        return _("Your password must contain at least a symbol.")
