from django.db import models
from goods.models import Goods
from user.models import User
from django.conf import settings


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    goods = models.ForeignKey(Goods)
    count = models.IntegerField()

    def get_total(self):
        '''获取小计'''
        return round(self.goods.price*self.count, 2)
