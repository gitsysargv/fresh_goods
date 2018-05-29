from django.conf.urls import url
from . import views

urlpatterns = [
    url('^add/$', views.add, name='add'),
    url(r'^$', views.cart_list_view, name='cart_edit'),
    url(r'^delete/$', views.delete_cart, name='delete'),
    url(r'^set/$', views.set_cart, name='set'),
]
