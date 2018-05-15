from django.db import models
from tinymce.models import HTMLField


class Type(models.Model):
    title = models.CharField('商品类型', max_length=20)

    def __str__(self):
        return self.title


class Goods(models.Model):
    title = models.CharField('商品名称', max_length=20)
    pic = models.ImageField('图片', upload_to='images/goods/')
    price = models.DecimalField('单价', max_digits=5, decimal_places=2)
    # isDelete = models.BooleanField(default=False)
    unit = models.CharField('单位', max_length=20, default='500g')
    click = models.IntegerField('点击量')
    intro = models.CharField('简介', max_length=200)
    repertory = models.IntegerField('库存')
    content = HTMLField('描述')
    type = models.ForeignKey(Type)

    # create_time = models.DateTimeField('创建时间', auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '商品'
        verbose_name_plural = "商品列表"
