from django.template import Library

register = Library()


def page_dict(page):
    index = page.number
    max_pages_num = page.paginator.num_pages
    dict_content = {'has_head': True, 'has_foot': True,
                    'range': []}
    if max_pages_num >= 5:  # 判断总页数是否大于5

        if index <= 3:  # 当前页面是否小于3
            dict_content['has_head'] = False
            dict_content['range'] = [1, 2, 3, 4, 5]
        elif 3 < index < max_pages_num - 2:
            dict_content['range'] = range(index - 2, index + 2 + 1)
        else:
            dict_content['has_foot'] = False
            dict_content['range'] = range(max_pages_num - 4, max_pages_num + 1)

    else:  # 如果最大页面小于5，则分页到最大页为止
        dict_content['has_head'] = False
        dict_content['has_foot'] = False
        dict_content['range'] = page.paginator.page_range
    return dict_content

register.filter('page_dict', page_dict)
