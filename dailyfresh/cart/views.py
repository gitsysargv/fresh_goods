import logging
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse

from .models import Cart


@login_required()
def add(request):
    '''是ajax的get方式添加购物车'''
    gid = request.GET.get('gid')
    count = request.GET.get('count')
    if gid is None or count is None:
        return JsonResponse({'isok': 0})
    else:
        try:
            gid = int(gid)
            count = int(count)
        except Exception as e:
            logger = logging.getLogger('django')
            logger.info('ajax发送的购物车数据不是整数! USER[{}] info:{}'.format(request.user, e))
            return JsonResponse({'isok': 0})

    carts = Cart.objects.filter(user=request.user, goods_id=gid)
    if len(carts) == 0:
        cart = Cart()
        cart.user = request.user
        cart.goods_id = gid
        cart.count = count
        cart.save()
    else:
        cart = carts[0]
        cart.count += count  # 同样的商品进行增加
        cart.save()

    return JsonResponse({'isok': 1})
