"""dailyfresh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from user import views as user_views

user_patterns = [
    url(r'^register/$', user_views.UserCreate.as_view(), name='register'),
    url(r'^repeat/$', user_views.username_is_repeat),
    url(r'^captcha/$', user_views.create_captcha_code, name='captcha'),
    url(r'^login/$', user_views.login, name='login'),
    url(r'^logout/$', user_views.logout_view, name='logout'),
    url(r'^user_center_info/$', user_views.UserDetail.as_view(), name='user_center_info'),
    url(r'^user_center_site/$', user_views.edit_recipients_address, name='user_center_site'),
]
goods_patterns = [

]

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'user/', include(user_patterns, namespace='user')),
    #  主页，即商品模块
    url(r'^', include(goods_patterns, namespace='goods')),
]
