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
    url(r'^register/$', user_views.UserCreate.as_view()),
    url(r'^captcha/$', user_views.create_captcha_code, name='captcha'),
    url(r'^user_center_info/$', user_views.UserDetail.as_view(), name='user_center_info')
]

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'user/', include(user_patterns, namespace='user'))
]