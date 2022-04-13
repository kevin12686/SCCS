from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import UserManager, AbstractBaseUser
from django.utils.translation import gettext_lazy as _


# Create your models here.

class ClimateControlUser(AbstractBaseUser):
    """
        An abstract base class implementing a fully featured User model with
        admin-compliant permissions.

        Username and password are required. Other fields are optional.
        """

    username_validator = MinLengthValidator(5)

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    is_admin = models.BooleanField(
        _("admin status"),
        default=False,
        help_text=_("Designates whether the user can has admin permissions."),
    )

    objects = UserManager()

    USERNAME_FIELD = "username"

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
