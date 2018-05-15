from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test import Client
from .models import User


class LoginViewTest(TestCase):
    def test_short_password_post(self):
        response = self.client.post('/user/login/', {'username': 'a', 'password': 'b'})
        self.assertContains(response, '密码长度小于6位')

    def test_invalid_post(self):
        response = self.client.post('/user/login/', {'username': 'a123', 'password': 'b987456321'})
        self.assertContains(response, '用户名或密码不正确', count=1)
        self.assertEqual(response.context['mark_name'], '')

    def test_invalid_post_with_mark_name(self):
        response = self.client.post('/user/login/', {'username': 'a123', 'password': 'b987456321', 'mark_name': '1'})
        self.assertContains(response, '用户名或密码不正确', count=1)
        self.assertContains(response, 'placeholder="请输入用户名" value="a123">')

    def test_correct_post(self):
        User.objects.create_user('chaiming', '', '123456789')
        response = self.client.post('/user/login/', {'username': 'chaiming', 'password': '123456789'})
        self.assertEqual(response.status_code, 302)
        # self.assertEqual(response.context['mark_name'], '')
