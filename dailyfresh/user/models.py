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


class RecipientsAddress(models.Model):
    user = models.ForeignKey(User)
    recipient = models.CharField('收件人', max_length=20)
    shipping_address = models.TextField('详细地址')
    postcode = models.CharField('邮编', max_length=6, blank=True, editable=False)
    mobile_number = models.CharField('手机', max_length=11,
                                     validators=[RegexValidator(
                                         r'^1[34578]\d{9}$', '手机格式不正确', 'invalid'
                                     )])
