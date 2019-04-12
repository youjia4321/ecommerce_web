from django.shortcuts import render, HttpResponse
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
import json
from django.views.generic.base import View
from users.forms import RegisterForm, LoginForm, ModifyPwdForm, ForgetForm, ChangeInfoForm
from users.models import UserProfile, EmailVerifyRecord
from django.contrib.auth.hashers import make_password, check_password
from utils.email_send import send_register_email
from django.db.models import Q
from django.contrib.auth import login, logout
from goods.models import GoodsInfo
from goods.views import show_image
# Create your views here.


def captcha():
    # 获取验证码，第一次请求，通过上面引用的CaptchaStore包 进行获取hashkey、image_url，以字典的形式返回
    hashkey = CaptchaStore.generate_key()
    image_url = captcha_image_url(hashkey)
    captcha = {'hashkey': hashkey, 'image_url': image_url}
    # print(captcha)s
    return captcha


def jarge_captcha(captchaStr, captchaHashkey):
    # 判断前端页面输入的验证码是否与数据库中的验证码相同，相同返回True，否则False
    if captchaStr and captchaHashkey:
        try:
            # 根据hsahkey获取数据库中的response
            get_captcha = CaptchaStore.objects.get(hashkey=captchaHashkey)

            # 如果验证码匹配
            if get_captcha.response == captchaStr.lower():
                return True
        except:
            return False
    else:
         return False


# 前端页面的ajax请求操作，点击刷新验证码
def refresh_captcha(request):
    return HttpResponse(json.dumps(captcha()), content_type='application/json')


def is_contain_chinese(check_str):
    # 判断字符串中是否包含中文（用于注册账号时输入用户名的判断）
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False


# 新用户注册
class RegisterView(View):
    # 以get的方式请求
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form, 'captcha': captcha()})

    # 以post的方式请求
    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            # 判断RegisterForm中定义的字段（forms.py文件）是否合法，例如是否不为空
            data = register_form.cleaned_data
            # register_form.cleaned_data包含了RegisterForm中定义的字段，
            # 跟前端页面表单中的name属性相对应，获取用户输入的值，字典形式返回
            if UserProfile.objects.filter(email=data['email']):
                # 判断数据库中是否有相同的email存在
                return render(request, 'register.html', {'register_form': register_form, 'captcha': captcha(), 'msg': '用户已存在'})

            flag = is_contain_chinese(data['username'])
            # 判断输入的用户名是否包含中文
            if not flag:
                if UserProfile.objects.filter(username=data['username']):
                    # 判断用户名username是否存在
                    return render(request, 'register.html', {'register_form': register_form, 'captcha': captcha(), 'msg': '此用户名已被使用'})

                captchaHashkey = request.POST.get('hashkey', '')
                if jarge_captcha(data['captcha'], captchaHashkey):
                    # 判断前端传过来的验证码是否与数据库中的相同
                    register_form.cleaned_data['password'] = make_password(register_form.cleaned_data['password'])
                    UserProfile.objects.create(**register_form.cleaned_data, is_active=False)
                    send_register_email(data['email'], 'register')
                    return render(request, 'login.html', {'msg': '发送邮件成功，请前往验证邮箱...', 'captcha': captcha()})
                    # 如果都满足的话，就渲染到login.html这个文件，反之就是下面的渲染到register.html文件并显示相应的错误
                else:
                    return render(request, 'register.html', {'register_form': register_form, 'msg': '验证码错误', 'captcha': captcha()})
            else:
                return render(request, 'register.html', {'register_form': register_form, 'captcha': captcha(), 'msg': '用户名不要包含中文'})
        else:
            return render(request, 'register.html', {'register_form': register_form, 'captcha': captcha()})


# 判断用户是否存在并且密码是否正确，满足的话就返回这个用户对象，不满足就返回None
def check(username=None, password=None):
    try:
        user = UserProfile.objects.get(Q(username=username) | Q(email=username))
        # 用户可以用email和username进行登录，引用Q 相当于or
        if user.check_password(password):
            return user
    except Exception as e:
        return None


# 用户登录操作 与注册操作大同小异
class LoginView(View):
    def get(self, request):
        login_form = LoginForm()
        return render(request, 'login.html', {'login_form': login_form, 'captcha': captcha()})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            data = login_form.cleaned_data
            user = check(username=data['username'], password=data['password'])
            # 判断用户是否存在且密码正确
            if user is not None:
                captchaHashkey = request.POST.get('hashkey', '')
                if jarge_captcha(data['captcha'], captchaHashkey):
                    if user.is_active:
                        # 判断用户是否验证
                        login(request, user)
                        # 登录此用户
                        ctx = show_image()
                        return render(request, 'index.html', ctx)
                    else:
                        return render(request, 'login.html', {'msg': '用户未验证', 'captcha': captcha(), 'login_form': login_form, })
                else:
                     return render(request, 'login.html', {'msg': '验证码错误', 'captcha': captcha(), 'login_form': login_form, })
            else:
                return render(request, 'login.html', {'msg': '用户不存在或密码错误', 'captcha': captcha(), 'login_form': login_form, })
        else:
            return render(request, 'login.html', {'login_form': login_form, 'captcha': captcha()})


# 用户注销
def Logout(request):
    logout(request)
    # 注销用户请求
    ctx =show_image()
    # show_image()方法是在goods.views下面的一个函数，作用是渲染主页index.html的对应的后台数据显示在前端
    return render(request, 'index.html', ctx)


# 激活用户
class ActiveView(View):
    def get(self, request, active_code):
        records = EmailVerifyRecord.objects.filter(code=active_code)
        # 获取后台数据库邮箱验证码这个表，查找是否有相同的code=active_code
        if records:
            for record in records:
                # 找到对应的email，找出这个用户，令用户的is_active字段为True，表示验证成功
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
            return render(request, 'login.html', {'msg': '用户已验证', 'captcha': captcha()})
        else:
            return render(request, 'active_fail.html')


# 进入到用户个人中心的接口
def self_info(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            # 判断用户是否登录
            user = request.user
            return render(request, 'self_info.html', {'user': user})
        else:
            return render(request, 'login.html', {'captcha': captcha()})


# 修改个人资料
def changeInfo(request):
    if request.method == 'POST':
        user = request.user
        username = request.POST.get('username', '')
        tel = request.POST.get('tel', '')
        oldpassword = request.POST.get('oldpassword', '')
        newpassword = request.POST.get('newpassword', '')
        mood = request.POST.get('mood', '')
        address = request.POST.get('address', '')
        if check_password(oldpassword, user.password):
            user.username = username
            user.mobile = tel
            user.password = make_password(newpassword)
            user.mood = mood
            user.address = address
            user.save()
            login(request, user)
            return render(request, 'self_info.html', {'user': user})
        return render(request, 'self_info.html', {'error': '密码错误'})
    


# 定义一个404方法，当输入的网址不存在时，则返回到404.html文件并在前端显示
def page_not_found(request):
    return render(request, '404.html')