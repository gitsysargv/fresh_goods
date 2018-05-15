# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=20, verbose_name='商品名称')),
                ('pic', models.ImageField(upload_to='images/goods/', verbose_name='图片')),
                ('price', models.DecimalField(max_digits=5, decimal_places=2, verbose_name='单价')),
                ('unit', models.CharField(default='500g', max_length=20, verbose_name='单位')),
                ('click', models.IntegerField(verbose_name='点击量')),
                ('intro', models.CharField(max_length=200, verbose_name='简介')),
                ('repertory', models.IntegerField(verbose_name='库存')),
                ('content', tinymce.models.HTMLField(verbose_name='描述')),
            ],
            options={
                'verbose_name_plural': '商品列表',
                'verbose_name': '商品',
            },
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=20, verbose_name='商品类型')),
            ],
        ),
        migrations.AddField(
            model_name='goods',
            name='type',
            field=models.ForeignKey(to='goods.Type'),
        ),
    ]
