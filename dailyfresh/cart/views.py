import logging
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse

from .models import Cart


def is_login_with_ajax(func):
    '''ajax方式的登陆验证'''
    def inner(request, *args, **kwargs):
        if request.user.is_authenticated():
            return func(request,  *args, **kwargs)
        else:
            return JsonResponse({'login': 0})
    return inner


@is_login_with_ajax
def add(request):
    '''是ajax的get方式添加购物车'''
    gid = request.GET.get('gid')
    count = request.GET.get('count')
    if gid is None or count is None:
        logger = logging.getLogger('django.client_error')
        logger.warning('需要的get参数不存在！')
        return JsonResponse({'isok': 0})
    else:
        try:
            gid = int(gid)
            count = int(count)
        except Exception as e:
            logger = logging.getLogger('django')
            logger.info('add增加购物车视图，ajax发送的数据不是整数! USER[{}] info:{}'.format(request.user, e))
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
    cart_count = request.user.cart_set.count()
    return JsonResponse({'isok': 1, 'cart_count': cart_count})


@login_required()
def cart_list_view(request):
    cart_list = request.user.cart_set.all()
    return render(request, 'cart/cart.html', locals())


@is_login_with_ajax
def delete_cart(request):
    cart_id = request.GET.get('cart_id')
    json_response_isok_not = JsonResponse({'isok': 0})
    if cart_id is None:
        logger = logging.getLogger('django.client_error')
        logger.warning('需要的get参数不存在！')
        return json_response_isok_not
    try:
        cart_id = int(cart_id)
    except Exception as e:
        logger = logging.getLogger('django')
        logger.warning('delete_cart删购物车视图，ajax发送的数据不是整数! USER[{}] info:{}'.format(request.user, e))
        return json_response_isok_not

    try:
        cart = Cart.objects.get(pk=cart_id)
    except Cart.DoesNotExist as e:
        logger = logging.getLogger('django')
        logger.warning('delete_cart删购物车视图，购物车ID不存在! USER[{}] info:{}'.format(request.user, e))
        return json_response_isok_not

    cart.delete()
    return JsonResponse({'isok': 1})


@is_login_with_ajax
def set_cart(request):
    '''ajax更改购物车里边的商品数量'''
    cid = request.GET.get('cid')
    count = request.GET.get('count')
    if cid is None or count is None:
        logger = logging.getLogger('django.client_error')
        logger.warning('需要的get参数不存在！')
        return JsonResponse({'isok': 0})
    try:
        cid = int(cid)
        count = int(count)
    except Exception as e:
        logger = logging.getLogger('django')
        logger.warning('set_cart更改视图，ajax数据不是整数字符串! USER[{}] info:{}'.format(request.user, e))
        return JsonResponse({'isok': 0})

    try:
        cart = Cart.objects.get(pk=cid)
    except Cart.DoesNotExist as e:
        logger = logging.getLogger('django')
        logger.warning('set_cart更改视图，购物车ID不存在! USER[{}] info:{}'.format(request.user, e))
        return JsonResponse({'isok': 0})

    cart.count = count
    cart.save()
    return JsonResponse({'isok': 1, 'count': count})
