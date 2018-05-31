from django.core.urlresolvers import reverse
from django.shortcuts import redirect


def is_has_carts(func):
    '''当没有购物车时进行跳转'''
    def inner(request, *args, **kwargs):
        if request.user.cart_set.exists():
            return func(request, *args, **kwargs)
        else:
            return redirect(reverse('cart:no-cart'))
    return inner
