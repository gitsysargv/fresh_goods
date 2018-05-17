from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from .models import GoodsType, Goods


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


def goods_list(request, id, sort, page):
    '''根据商品类型返回商品列表
    id: 商品类型ID
    sort: 排序方式  2价格， 3 人气, 1 和其他情况为默认
    page_index: 页码 
    context: news 商品最新的两个
            page 分页
            '''
    # print(sort)
    goods_type = get_object_or_404(GoodsType, pk=id)
    if sort == '3' or sort is None:
        sort_list = goods_type.goods_set.order_by('-click')
    elif sort == '2':
        sort_list = goods_type.goods_set.order_by('price')
    else:
        sort_list = goods_type.goods_set.order_by('-id')

    if page is None or page == '1':
        page_index = 1
    else:
        page_index = int(page)
    paginator = Paginator(sort_list, 15)
    if page_index not in paginator.page_range:
        page_index = 1
    context = {'page': paginator.page(page_index),
               'news': goods_type.goods_set.order_by('-id')[0:2]}
    return render(request, 'goods/list.html', context)


def goods_detail(request):
    return render(request, 'goods/detail.html')
