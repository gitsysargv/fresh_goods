import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_POST

from cart.models import Cart


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
        logger.warning('post参数-- 购物车ID：cid 为空！')
    cart_list = []
    try:
        for cid in cart_id_list:
            cid = int(cid)
            cart = Cart.objects.get(pk=cid)
            cart_list.append(cart)
    except Cart.DoesNotExist as e:
        logger = logging.getLogger('django.client_error')
        logger.error('购物车ID不存在！USER[{}], ID由购物车编辑页提交'.format(request.user))
        cart_list = []
    except Exception as e:
        logger = logging.getLogger('django.client_error')
        logger.warning('购物车ID不是整数！USER[{}], Exception[{}]'.format(request.user, e))
        cart_list = []
    return render(request, template_name, {'cart_list': cart_list})
