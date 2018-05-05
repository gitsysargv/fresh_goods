#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ""
__author__ = "chaiming"
__mtime__ = "2018/5/3"
# code is far away from bugs with the god animal protecting
I love animals. They taste delicious.
┏┓ ┏┓
┏┛┻━━━┛┻┓
┃ ☃ ┃
┃ ┳┛ ┗┳ ┃
┃ ┻ ┃
┗━┓ ┏━┛
┃ ┗━━━┓
┃ 神兽保佑 ┣┓
┃　永无BUG！ ┏┛
┗┓┓┏━┳┓┏┛
┃┫┫ ┃┫┫
┗┻┛ ┗┻┛
"""
from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from .models import User


class UserModelRegisterForm(ModelForm):
    password = forms.CharField(label='密码', max_length=20, min_length=6,
                               validators=[
                                   validators.RegexValidator(r'^[\w\d_]+$', '由字母,数字和下划线不低于6位的字符组成', 'invalid')
                               ],
                               error_messages={'min_length': '密码长度小于6位', 'max_length': '密码长度大于20位'},
                               widget=forms.PasswordInput)
    cpwd = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(label='电子邮箱')
    # captcha = forms.CharField(label='验证码', help_text='验证是否是机器人')
    agree = forms.BooleanField(label='同意', error_messages={'required': '未勾选'})
    x1 = forms.IntegerField()
    x2 = forms.IntegerField()
    x3 = forms.IntegerField()
    y1 = forms.IntegerField()
    y2 = forms.IntegerField()
    y3 = forms.IntegerField()

    error_css_class = 'error'
    required_css_class = 'required'

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def valid_captcha(self, code):
        if all(
                [
                                    code.get('x1') <= int(self.cleaned_data.get('x1')) <= code.get('x1') + code.get('size'),
                                    code.get('x2') <= int(self.cleaned_data.get('x2')) <= code.get('x2') + code.get('size'),
                                    code.get('x3') <= int(self.cleaned_data.get('x3')) <= code.get('x3') + code.get('size'),
                                    code.get('y1') <= int(self.cleaned_data.get('y1')) <= code.get('y1') + code.get('size'),
                                    code.get('y2') <= int(self.cleaned_data.get('y2')) <= code.get('y2') + code.get('size'),
                                    code.get('y3') <= int(self.cleaned_data.get('y3')) <= code.get('y3') + code.get('size'),
                ]
        ):
            return True
        else:
            validation_error = ValidationError('请按顺序文字', code='invalid')
            '''点击验证，直接把错误信息插入第一条坐标的验证字段里'''
            self.add_error('x1', validation_error)
            return False

    def clean_username(self):
        data = self.cleaned_data.get('username')
        if User.objects.filter(username=data).exists():
            raise ValidationError('用户名已存在', code='invalid')

        return data  # always return the cleaned data

    def clean(self):
        cleaned_data = super().clean()
        '''ModelForm.clean() 方法设置一个标识符， 
        使得模型验证 这一步验证标记为unique、 unique_together 或
        unique_for_date|month|year 的模型字段的唯一性。
        如果你需要覆盖clean() 方法并维持这个验证行为，你必须调用父类的clean() 方法。'''

        if self.cleaned_data.get('password') != self.cleaned_data.get('cpwd'):
            raise ValidationError('两个密码不相同')
