from django.db import models
from django.conf import settings

from goods.models import Goods


class OrderForm(models.Model):
    '''订单编号：由当前时间+用户编号构成,主键
    订单用户 
    下单日期
    是否支付
    支付方式：货到付款，微信支付，支付宝，银行卡
    金额总计
    收获订址'''
    order_number = models.CharField('订单编号', max_length=20, primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    order_date = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    '''Modes of Payment'''
    MODES_OF_PAYMENT = (
        ('HDFK', '货到付款'),
        ('WX', '微信支付'),
        ('ZFB', '支付宝'),
        ('YHK', '银行卡'),
    )
    payment = models.CharField(max_length=10, choices=MODES_OF_PAYMENT, default='HDFK')
    # 最大千位数9999.99
    total = models.DecimalField(max_digits=6, decimal_places=2)
    shipping_address = models.TextField('收获订址')


class OrderContent(models.Model):
    '''每份关联订单的购物车详情
    关联商品
    数量
    价格
    关联订单
    '''
    goods = models.ForeignKey(Goods)
    count = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    order = models.ForeignKey(OrderForm)
