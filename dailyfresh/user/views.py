import random
from io import BytesIO
import logging

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.core import signing
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse_lazy, reverse
from django.template.response import TemplateResponse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.http import last_modified
from django.views.generic import FormView, TemplateView, DetailView

from goods.models import Goods
from .models import User, RecipientsAddress
from .form import UserModelRegisterForm, UserLoginForm
from PIL import Image, ImageDraw, ImageFont, ImageFilter


def create_captcha_code(request):
    '''
    生成 4个汉字验证码 ,需要用户按顺序点击其中的 3个
    保存到会话中 
    返回验证码图片'''

    # 随机的4个汉字:
    zh_words = ['牛', '国', '王', '有', '天', '好', '吉', '祥', '如', '意']
    zh_words = random.sample(zh_words, 4)

    #  画图
    image = Image.open(r'C:\Users\chaiming\Desktop\IMG_20170502_165107_344.jpg')

    # w, h = image.size
    # image.thumbnail((w // 2, h // 2))

    # 随机颜色
    def rnd_color():
        return (random.choice([0, 255]), 0, random.choice([0, 255]))

    # 创建Font对象: 大小为长宽中小的那个的8/1
    width, height = image.size
    font_size = int(min(image.size)) // 8
    font = ImageFont.truetype(r'F:\pycharm_projects\djcode\dailyfresh\user\fonts\MSYH.TTF', font_size)
    # 创建Draw对象:
    draw = ImageDraw.Draw(image)

    # 生成随机坐标
    x1 = random.randint(0, width - font_size)
    y1 = random.randint(0 + font_size, height - font_size)
    # 循环3次，把剩下的符合的坐标提取
    points_list = [(x1, y1)]
    for i in range(3):
        is_not_pass = True
        while is_not_pass:
            x2, y2 = random.randint(0, width - font_size), random.randint(0 + font_size, height - font_size)
            for x, y in points_list:
                if (x2 > x + font_size) or (x2 + font_size < x) or (y2 > y + font_size) or (y2 + font_size < y):
                    pass

                else:
                    is_not_pass = True
                    break
            else:
                is_not_pass = False
                points_list.append((x2, y2))

    # 输出文字:
    for t in range(4):
        draw.text(points_list[t], zh_words[t], font=font,
                  fill=rnd_color())

    z_p = zip(zh_words, points_list)  # 把字和坐标组合
    sample = random.sample([i for i in z_p], 3)

    #  设置session 在后端验证
    captcha_dict = {
        'a1': sample[0][0], 'x1': sample[0][1][0], 'y1': sample[0][1][1],
        'a2': sample[1][0], 'x2': sample[1][1][0], 'y2': sample[1][1][1],
        'a3': sample[2][0], 'x3': sample[2][1][0], 'y3': sample[2][1][1],
        'size': font_size
    }

    # 模糊:
    # image = image.filter(ImageFilter.BLUR)
    # del draw
    # draw = ImageDraw.Draw(image)
    draw.text(
        (0, 0),
        '"{}", "{}", "{}"'.format(captcha_dict['a1'], captcha_dict['a2'], captcha_dict['a3']),
        font=font,
        fill=(0, 0, 0)
    )

    buff = BytesIO()
    image.save(buff, 'jpeg')
    response = HttpResponse(buff.getvalue(), 'image/jpeg')

    request.session['captcha'] = captcha_dict

    return response


class UserCreate(FormView):
    form_class = UserModelRegisterForm
    template_name = 'user/register.html'
    success_url = reverse_lazy('user:user_center_info')  # 跳转到用户中心

    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super(UserCreate, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        #  对验证码进行验证
        code = self.request.session.get('captcha')
        if code:
            ret = form.valid_captcha(code=code)
        else:
            logger = logging.getLogger('captcha')
            logger.warning('IP: {}, 主机: {}, 服务器认证后的用户: {} 客户端篡改Cookies'.format(
                self.request.META.get('REMOTE_ADDR'),
                self.request.META.get('REMOTE_HOST'),
                self.request.META.get('REMOTE_USER'),
            ))
            raise Http404

        if ret is False:
            return render(self.request, self.template_name, {'form': form})

        User.objects.create_user(
            form.cleaned_data.get('username'),
            form.cleaned_data.get('email'),
            form.cleaned_data.get('password'),
        )
        return super().form_valid(form)  # 验证成功后调用, 默认返回成功的重定向


def username_is_repeat(request):
    '''ajax验证同名用户功能'''
    if User.objects.filter(username=request.GET.get('username')).exists():
        return JsonResponse({'is_repeat': 1})
    return JsonResponse({'is_repeat': 0})


class UserLogin(FormView):
    form_class = UserLoginForm
    template_name = 'user/login.html'
    success_url = reverse_lazy('user:user_center_info')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mark_name'] = self.request.get_signed_cookie('mark_name', '')
        return context

    def form_valid(self, form):
        user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
        if user is not None:
            if user.is_active:
                #  用户登陆
                auth_login(self.request, user)
                #  重定向
                return super().form_valid(form)
        else:
            #  用户验证不成功
            form.add_error(None, '用户名或密码不正确')
            context = {}

            response = TemplateResponse(self.request, self.template_name, context)

            # print(response.context_data)
            #  如果勾选了记住用户名，则保存到Cookies中, key=mark_name, 如果未勾选，设置mark_name 为空
            username = self.request.POST.get('username')
            if self.request.POST.get('mark_name') == '1':
                response.set_signed_cookie('mark_name', username)
            else:
                response.delete_cookie('mark_name')
                username = ''

            context = {
                'form': form,
                'mark_name': username
            }
            response.context_data = context
            return response

            #  直接调用 self.form_invalid()
            # return self.form_invalid(form)

    def form_invalid(self, form):
        context = {}
        response = TemplateResponse(self.request, self.template_name, context)
        #  如果勾选了记住用户名，则保存到Cookies中, key=mark_name
        username = self.request.POST.get('username')
        if self.request.POST.get('mark_name') == '1':
            response.set_signed_cookie('mark_name', username)
        else:
            response.delete_cookie('mark_name')
            username = ''

        context = {
            'form': form,
            'mark_name': username
        }
        response.context_data = context
        return response


def login_datetime(request):
    return timezone.datetime(2018, 5, 20)  # 登陆页面最后修改时间


@last_modified(login_datetime)
@never_cache
def login(request):
    template_name = 'user/login.html'
    success_url = reverse_lazy('user:user_center_info')  # 跳转到用户中心
    if request.method == 'GET':
        return render(request, template_name, {'mark_name': request.get_signed_cookie('mark_name', '')})

    else:
        username = request.POST.get('username')
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    #  登陆
                    auth_login(request, user)
                    #  重定向, 获取装饰器login_required 的next参数，实现跳转到登陆之前的路径
                    success_url = request.GET.get('next', success_url)
                    response = redirect(success_url)
                    #  记住用户名功能
                    if request.POST.get('mark_name') == '1':
                        response.set_signed_cookie('mark_name', username)
                    else:
                        response.delete_cookie('mark_name')
                    return response
            else:
                form.add_error(None, '用户名或密码不正确')
        #  页面记住用户名功能，把用户名存在cookie里
        response = TemplateResponse(request, template_name, {})

        if request.POST.get('mark_name') == '1':
            response.set_signed_cookie('mark_name', username)
        else:
            response.delete_cookie('mark_name')
            username = ''
        response.context_data = {'form': form, 'mark_name': username}
        return response


'''
头部Last-Modified 格式化
Expires: Thu, 10 May 2018 10:17:09 GMT
response['Last-Modified'] = timezone.datetime(2018, 5, 8).strftime('%a, %d %b %Y %H:%M:%S GMT')
'''


def logout_view(request):
    '''登出视图'''
    auth_logout(request)
    # Redirect to a success page.
    next_path = request.GET.get('next')
    if next_path:
        return redirect('%s?next=%s' % (reverse('user:login'), next_path))
    else:
        return redirect(reverse('user:login'))


class UserDetail(TemplateView):
    template_name = 'user/user_center_info.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        signing_str = self.request.COOKIES.get('gid_list')
        if signing_str is not None:
            try:
                gid_list = signing.loads(signing_str)
            except signing.BadSignature as e:
                logger = logging.getLogger('django.cookies')
                logger.warning('cookies中获取gid错误：{}, USER[{}], REMOTE_ADDR[{}]'.format(
                    e,
                    self.request.user,
                    self.request.META.get('REMOTE_ADDR'),
                ))
                gid_list = []
        else:
            gid_list = []

        recently_viewed = []
        if gid_list is not []:
            for gid in gid_list:
                try:
                    goods = Goods.objects.get(pk=gid)
                except Goods.DoesNotExist:
                    goods = None
                if goods is not None:
                    recently_viewed.append(goods)

        context['recently_viewed'] = recently_viewed
        return context

    # def get(self, request, *args, **kwargs):
    #     self.cookies = request.COOKIES
    #     return super().get(request, *args, **kwargs)


@login_required()
def edit_recipients_address(request):
    if request.method == 'POST':
        recipients_address = RecipientsAddress(
            user=request.user,
            recipient=request.POST.get('recipient', ''),
            shipping_address=request.POST.get('shipping_address', ''),
            postcode=request.POST.get('postcode', ''),
            mobile_number=request.POST.get('mobile_number', ''),
        )
        recipients_address.save()
    return render(request, 'user/user_center_site.html')
