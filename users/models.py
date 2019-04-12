from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
# Create your models here.


class UserProfile(AbstractUser):          
    birthday = models.DateField(null=True, blank=True, verbose_name='生日')
    image = models.ImageField(upload_to="the_avatars", default='the_avatars/default.jpg', max_length=100, verbose_name='头像')
    mood = models.CharField(max_length=300, default='暂无签名', verbose_name='个性签名')
    gender = models.CharField(max_length=6, choices=(('male', '男'), ('female', '女')), default='female', verbose_name='性别')
    address = models.CharField(max_length=100, default='暂无', verbose_name='地址')
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name='联系方式')
    money = models.IntegerField(default=10000, verbose_name='账户余额')
    captcha = models.CharField(max_length=10, default='', verbose_name='验证码')

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class Address(models.Model):
    address = models.CharField(max_length=150, verbose_name='地址')
    user = models.ManyToManyField(UserProfile, related_name='user_address', verbose_name='地址', blank=True)

    class Meta:
        verbose_name = '用户订购地址'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.address


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name="验证码")
    email = models.EmailField(max_length=50, verbose_name="邮箱")
    send_type = models.CharField(verbose_name="验证码类型", max_length=10, choices=(("register", "注册"), ("forget", "忘记密码")))
    send_time = models.DateTimeField(verbose_name="发送时间", default=datetime.now)

    class Meta:
        verbose_name = "邮箱验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}({1})'.format(self.code, self.email)
