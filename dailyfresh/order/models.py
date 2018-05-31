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
    收获订址
    订单根据创建时间降序排列'''
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
    # 最大万位数99999.99
    total = models.DecimalField(max_digits=7, decimal_places=2)
    shipping_address = models.CharField('收获订址', max_length=150)

    class Meta:
        ordering = ['-order_date']

    # 进行支付方式的设置
    def set_payment(self, pay):
        for pay_tuple in self.MODES_OF_PAYMENT:
            if pay_tuple[0] == pay:
                self.payment = pay
            else:
                self.payment = 'HDFK'


class OrderCart(models.Model):
    '''每份关联订单的购物车详情
    关联商品
    数量
    价格
    关联订单
    '''
    goods = models.ForeignKey(Goods)
    # 或者只保存商品名称, 不过会增加数据库的大小
    # goods_title = models.CharField(max_length=20)
    count = models.IntegerField()
    # 商品的价格有可能因为促销等原因有变动
    # max_digits=5 和Goods模型里边的一样
    price = models.DecimalField(max_digits=5, decimal_places=2)
    order = models.ForeignKey(OrderForm)

    def get_total(self):
        '''获取小计'''
        return round(self.price*self.count, 2)
