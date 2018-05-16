from django.shortcuts import render
from django.views.generic import ListView

from .models import GoodsType


def home_page(request):
    '''主页
    显示商品列表: 目前共有6种类型
    （新鲜水果，海鲜水产，猪牛羊肉，禽类蛋品，新鲜蔬菜，速冻食品）
    1. 显示3个最有人气（点击量）商品
    2. 显示4个最新商品
    '''
    template_name = 'goods/index.html'
    #  新鲜水果
    fruit = GoodsType.objects.get(pk=1)
    fruit_click = fruit.get_click_list(3)
    fruit_new = fruit.get_new_list(4)
    # 海鲜水产
    seafood = GoodsType.objects.get(pk=2)
    seafood_click = seafood.get_click_list(2)
    seafood_new = seafood.get_new_list(4)

    # 猪牛羊肉
    meat = GoodsType.objects.get(pk=3)
    meat_click = meat.get_click_list(3)
    meat_new = meat.get_new_list(4)

    # 禽类蛋品
    egg = GoodsType.objects.get(pk=4)
    egg_click = egg.get_click_list(3)
    egg_new = egg.get_new_list(4)

    # 新鲜蔬菜
    vegetable = GoodsType.objects.get(pk=5)
    vegetable_click = vegetable.get_click_list(3)
    vegetable_new = vegetable.get_new_list(4)

    # 速冻食品
    quick_frozen_food = GoodsType.objects.get(pk=6)
    quick_frozen_food_click = quick_frozen_food.get_click_list(3)
    quick_frozen_food_new = quick_frozen_food.get_new_list(4)

    context = {
        'fruit': fruit,
        'fruit_click': fruit_click,
        'fruit_new': fruit_new,
        'seafood': seafood,
        'seafood_click': seafood_click,
        'seafood_new': seafood_new,
        'meat': meat,
        'meat_click': meat_click,
        'meat_new': meat_new,
        'egg': egg,
        'egg_click': egg_click,
        'egg_new': egg_new,
        'vegetable': vegetable,
        'vegetable_click': vegetable_click,
        'vegetable_new': vegetable_new,
        'quick_frozen_food': quick_frozen_food,
        'quick_frozen_food_click': quick_frozen_food_click,
        'quick_frozen_food_new': quick_frozen_food_new,
    }
    return render(request, template_name, context)
