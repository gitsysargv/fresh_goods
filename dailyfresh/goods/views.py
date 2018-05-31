import logging
from django.core import signing
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page
# from django.views.decorators.http import condition
from django.views.generic import ListView

from .models import GoodsType, Goods


@cache_page(60 * 60 * 3)  # 缓存3个小时
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


# def goods_list_etag(request, tid, sort, page_index):
#     goods = Goods.objects.only('id').last()
#     goods_id = 0
#     if goods is not None:
#         goods_id = goods.id
#     etag = str(tid) + str(sort) + str(page_index) + str(goods_id)
#     return etag
#
#
# @condition(etag_func=goods_list_etag)
@cache_page(60 * 60 * 1)  # 缓存1个小时
def goods_list(request, tid, sort, page_index):
    '''根据商品类型返回商品列表
    tid: 商品类型ID
    sort: 排序方式  2价格， 3 人气, 1 和其他情况为默认
    page_index: 页码 
    context: news 商品最新的两个
            page 分页
            '''
    # print(sort)  捕获不到时sort 为None
    goods_type = get_object_or_404(GoodsType, pk=tid)
    if sort == '3':
        sort_list = goods_type.goods_set.order_by('-click')
    elif sort == '2':
        sort_list = goods_type.goods_set.order_by('price')
    else:
        sort = '1'
        sort_list = goods_type.goods_set.order_by('-id')

    if page_index is None or page_index == '1':
        page_index = 1

    paginator = Paginator(sort_list, 2)
    try:
        content = paginator.page(page_index)
    except PageNotAnInteger:
        content = paginator.page(1)
    except EmptyPage:
        #  如果页面不在范围内，返回最后一页paginator.num_pages
        content = paginator.page(paginator.num_pages)
    # print(page_index)
    # print(content.number)
    # print(paginator.num_pages)
    #  根据当前页码设计首页，尾页
    has_head = has_foot = True
    #  构造页面范围
    if paginator.num_pages >= 5:  # 判断总页数是否大于5

        if content.number <= 3:  # 当前页面是否小于3
            page_range = [1, 2, 3, 4, 5]
            has_head = False
        elif 3 < content.number < paginator.num_pages - 2:
            page_range = range(content.number - 2, content.number + 2 + 1)
        else:
            page_range = range(paginator.num_pages - 4, paginator.num_pages + 1)
            has_foot = False
    else:  # 如果最大页面小于5，则分页到最大页为止
        page_range = paginator.page_range
        has_head = False
        has_foot = False

    context = {'page': content,
               'news': goods_type.goods_set.order_by('-id')[0:2],
               'goods_type': goods_type,
               'sort': sort,
               'page_range': page_range,
               'has_head': has_head,
               'has_foot': has_foot}
    return render(request, 'goods/list.html', context)


def goods_detail(request, gid):
    goods = get_object_or_404(Goods, pk=gid)
    news = goods.type.goods_set.only('id', 'title', 'pic', 'price').order_by('-id')[0:2]
    '''保存几个个gid到COOKIES中，最大5位，列表类型：[1,2,3,4,5]'''
    signing_str = request.COOKIES.get('gid_list')
    if signing_str is not None:
        try:
            gid_list = signing.loads(signing_str)
        except signing.BadSignature as e:
            logger = logging.getLogger('django.cookies')
            logger.warning('cookies中获取gid错误：{}, USER[{}], REMOTE_ADDR[{}]'.format(
                e,
                request.user,
                request.META.get('REMOTE_ADDR'),
            ))
            gid_list = []
    else:
        gid_list = []

    if len(gid_list) == 5:
        # 当id已经存在就什么都不做
        if gid not in gid_list:
            gid_list.insert(0, gid)
            gid_list.pop()
    else:
        if gid not in gid_list:
            gid_list.insert(0, gid)
    response = render(request, 'goods/detail.html', locals())
    response.set_cookie('gid_list', signing.dumps(gid_list), max_age=60*60*24*15)
    return response
