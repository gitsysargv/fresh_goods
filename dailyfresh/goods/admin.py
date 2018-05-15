from django.contrib import admin
from .models import Goods


class GoodsAdmin(admin.ModelAdmin):
    list_per_page = 20
    # fields = ['title', 'price', 'unit', 'click', 'repertory']
    list_display = ['id', 'title', 'price', 'unit', 'click', 'repertory']


admin.site.register(Goods, GoodsAdmin)
