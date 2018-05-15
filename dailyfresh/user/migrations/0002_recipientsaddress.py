# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecipientsAddress',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('recipient', models.CharField(max_length=20, verbose_name='收件人')),
                ('shipping_address', models.TextField(verbose_name='详细地址')),
                ('postcode', models.CharField(blank=True, max_length=6, editable=False, verbose_name='邮编')),
                ('mobile_number', models.CharField(validators=[django.core.validators.RegexValidator('^1[34578]\\d{9}$', '手机格式不正确', 'invalid')], max_length=11, verbose_name='手机')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
