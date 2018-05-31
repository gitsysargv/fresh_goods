import logging
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from django.db import transaction
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from cart.models import Cart
from django.views.generic import TemplateView

from .models import OrderForm, OrderCart
from user.models import RecipientsAddress


@login_required()
@require_POST
def checked_cart_list_view(request):
    template_name = 'order/place_order.html'
    cart_id_list = request.POST.getlist('cid')
    # print(type(cart_id_list))
    # if cart_id_list == []:
    #     print('调---------')
    # if cart_id_list is []:  事实证明用 is []来判断是错的
    if len(cart_id_list) == 0:
        logger = logging.getLogger('django.client_error')
        logger.warning('[order视图] post参数-- 购物车ID：cid 为空！')
    cart_list = []
    try:
        for cid in cart_id_list:
            cid = int(cid)
            cart = Cart.objects.get(pk=cid)
            cart_list.append(cart)
    except Cart.DoesNotExist as e:
        logger = logging.getLogger('django.client_error')
        logger.error('[order视图] 购物车ID不存在！USER[{}], ID由购物车编辑页提交'.format(request.user))
        cart_list = []
    except Exception as e:
        logger = logging.getLogger('django.client_error')
        logger.warning('[order视图] 购物车ID不是整数！USER[{}], Exception[{}]'.format(request.user, e))
        cart_list = []

    if len(cart_list) == 0:
        messages.add_message(request, messages.ERROR, '购物车不存在！')
        return redirect(reverse('order:order-error'))
    # print(cart_list, id(cart_list), id([]))

    return render(request, template_name, {'cart_list': cart_list})


class LowStocks(Exception):
    def __init__(self, err_msg, goods_title):
        self.err_msg = err_msg
        self.goods_title = goods_title


@login_required()
@require_POST
def handle_view(request):
    address_id = request.POST.get('address')
    pay_style = request.POST.get('pay_style')  # 支付方式
    cart_id_list = request.POST.getlist('cid')  # ID列表
    '''处理支付方式'''
    if pay_style is None:
        messages.add_message(request, messages.ERROR, '请勾选支付方式！')
        return redirect(reverse('order:order-error'))
    '''编辑收件人地址'''
    try:
        address_id = int(address_id)
    except Exception:
        logger = logging.getLogger('django.client_error')
        logger.warning('[order视图] post参数-- 收件人地址的ID：不是一个整数字符串！')
        # 跳转错误页面
        messages.add_message(request, messages.ERROR, '请勾选收获地址!')
        return redirect(reverse('order:order-error'))
    try:
        address = RecipientsAddress.objects.get(pk=address_id)
    except RecipientsAddress.DoesNotExist:
        logger = logging.getLogger('django.client_error')
        logger.warning('[order视图] post参数-- 收件人地址的ID：address 数据有误！')
        # 跳转错误页面
        messages.add_message(request, messages.ERROR, '请勾选收获地址!')
        return redirect(reverse('order:order-error'))

    shipping_address = '''{} （{} 收） {}'''.format(
        address.shipping_address,
        address.recipient,
        address.mobile_number
    )

    '''通过POST参数获取，购物车列表'''
    if len(cart_id_list) == 0:
        logger = logging.getLogger('django.client_error')
        logger.warning('[order视图] post参数-- 购物车ID：cid 为空！')
        messages.add_message(request, messages.ERROR, '购物车不存在!')
        return redirect(reverse('order:order-error'))
    cart_list = []
    try:
        for cid in cart_id_list:
            cid = int(cid)
            cart = Cart.objects.get(pk=cid)
            cart_list.append(cart)
    except Cart.DoesNotExist as e:
        logger = logging.getLogger('django.client_error')
        logger.warning('[order视图] 购物车ID不存在！USER[{}], ID由购物车编辑页提交'.format(request.user))
        cart_list = []
    except (TypeError, ValueError) as e:
        logger = logging.getLogger('django.client_error')
        logger.warning('[order视图] 购物车ID不是整数！USER[{}], Exception[{}]'.format(request.user, e))
        cart_list = []

    if len(cart_list) == 0:
        messages.add_message(request, messages.ERROR, '购物车不存在!')
        return redirect(reverse('order:order-error'))
    '''构建订单模型,
        --构造相关联的详单模型，如果库存不足则回滚
            --每次删除一个购物车
    '''
    try:
        with transaction.atomic():
            order_form = OrderForm()

            order_form.order_number = datetime.today().strftime('%Y%m%d%H%M%S') + str(request.user.id)  # 订单表的主键
            order_form.user = request.user
            order_form.set_payment(pay_style)
            order_form.total = 0
            order_form.shipping_address = shipping_address
            order_form.save()

            # 计数支付金额total, 创建订单的每一份详情
            total = 0
            for cart in cart_list:
                if cart.goods.repertory < cart.count:  # 如果商品的库存 小于 购物车里的数量, 进行回滚操作
                    raise LowStocks('商品库存不足!', cart.goods.title)

                order_cart = OrderCart()
                order_cart.goods = cart.goods
                order_cart.count = cart.count
                order_cart.price = cart.goods.price
                order_cart.order = order_form
                order_cart.save()
                total += cart.get_total()

                cart.delete()  # 删除购物车

            order_form.total = total
            order_form.save()
    except LowStocks as error:
        #  库存不足返回购物车编辑页面
        logger = logging.getLogger('django.client_error')
        logger.error('[order视图] 商品goods[{}] msg:{}!'.format(error.goods_title, error.err_msg))
        messages.add_message(request, messages.ERROR, '库存不足!')
        return redirect(reverse('order:order-error'))

    return redirect(reverse('order:user_center_order'))  # 跳转到用户的订单页面


def user_center_order(request, index):
    template_name = 'user/user_center_order.html'
    paginator = Paginator(request.user.orderform_set.all(), 3)

    if index is None:
        index = 1
    try:
        page = paginator.page(index)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(1)
    return render(request, template_name, {'page': page})


class OrderErrorView(TemplateView):
    '''订单错误页面'''
    template_name = 'order/order_error_messages.html'
