# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('goods', '0002_auto_20180516_1719'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderCart',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('count', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('goods', models.ForeignKey(to='goods.Goods')),
            ],
        ),
        migrations.CreateModel(
            name='OrderForm',
            fields=[
                ('order_number', models.CharField(serialize=False, max_length=20, verbose_name='订单编号', primary_key=True)),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('is_paid', models.BooleanField(default=False)),
                ('payment', models.CharField(default='HDFK', max_length=10, choices=[('HDFK', '货到付款'), ('WX', '微信支付'), ('ZFB', '支付宝'), ('YHK', '银行卡')])),
                ('total', models.DecimalField(decimal_places=2, max_digits=7)),
                ('shipping_address', models.CharField(max_length=150, verbose_name='收获订址')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='ordercart',
            name='order',
            field=models.ForeignKey(to='order.OrderForm'),
        ),
    ]
