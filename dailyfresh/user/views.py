import random
from io import BytesIO

from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse_lazy
from django.views.generic import FormView, TemplateView, DetailView

from .models import User
from .form import UserModelRegisterForm
from PIL import Image, ImageDraw, ImageFont, ImageFilter


def create_captcha_code(request):
    '''生成验证码 保存到会话中 返回验证码图片'''

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
    # 模糊:
    image = image.filter(ImageFilter.BLUR)

    z_p = zip(zh_words, points_list)  # 把字和坐标组合
    sample = random.sample([i for i in z_p], 3)

    #  设置session 在后端验证
    captcha_dict = {
        'a1': sample[0][0], 'x1': sample[0][1][0], 'y1': sample[0][1][1],
        'a2': sample[1][0], 'x2': sample[1][1][0], 'y2': sample[1][1][1],
        'a3': sample[2][0], 'x3': sample[2][1][0], 'y3': sample[2][1][1],
        'size': font_size
    }

    del draw
    draw = ImageDraw.Draw(image)
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
    success_url = reverse_lazy('user:user_center_info')

    # def get(self, request, *args, **kwargs):
    #     code = create_captcha_code()
    #     request.session['captcha'] = code
    #     return super().get(request, *args, **kwargs)

    # 验证成功后调用, 默认返回成功的重定向
    def form_valid(self, form):
        code = self.request.session.get('captcha')
        ret = form.valid_captcha(code=code)

        if ret is False:
            return render(self.request, self.template_name, {'form': form})

        User.objects.create_user(
            form.cleaned_data.get('username'),
            form.cleaned_data.get('email'),
            form.cleaned_data.get('password'),
        )
        return super().form_valid(form)


class UserDetail(TemplateView):
    template_name = 'user/user_center_info.html'
