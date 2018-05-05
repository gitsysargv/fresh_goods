from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class User(AbstractUser):
    """
    Users within the Django authentication system are represented by this
    model.

    Username, password and email are required. Other fields are optional.
    """
    mobile_number = models.CharField('手机号码', max_length=11,
                                     null=True, blank=True,
                                     validators=[RegexValidator(
                                         r'^\d{11}$', '手机格式不正确', 'invalid'
                                     )])
    address = models.CharField('联系地址', max_length=100, null=True, blank=True)

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
