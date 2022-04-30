from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils.translation import gettext_lazy as _


# Create your models here.

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError('The given username must be set.')
        username = self.model.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, is_admin, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', is_admin)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser must have is_admin=True.')
        return self._create_user(username, password, **extra_fields)


class ClimateControlUser(AbstractBaseUser):
    username_validator = MinLengthValidator(5)

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_(
            'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'
        ),
        validators=[username_validator],
        error_messages={
            'unique': _('A user with that username already exists.'),
        },
    )
    is_admin = models.BooleanField(
        _('admin status'),
        default=False,
        help_text=_('Designates whether the user can has admin permissions.'),
    )

    objects = UserManager()

    USERNAME_FIELD = 'username'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')


class History(models.Model):
    temperature = models.PositiveSmallIntegerField(verbose_name='Temperature')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Time')

    class Meta:
        verbose_name = _('history')
        verbose_name_plural = _('history')
