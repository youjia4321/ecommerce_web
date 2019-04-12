from django.db import models
from users.models import UserProfile
from datetime import datetime
# Create your models here.


# 数据库中的银行卡的字段
class CardInfo(models.Model):
    user = models.ForeignKey(UserProfile, related_name='user_card', verbose_name='持卡人', on_delete=models.CASCADE)
    card_id = models.CharField(max_length=18, verbose_name="卡号")
    card_password = models.CharField(max_length=128, verbose_name="密码")
    card_money = models.IntegerField(verbose_name="金钱余额", default='0')
    open_time = models.DateTimeField(verbose_name="开户时间", default=datetime.now)
    is_active = models.BooleanField(verbose_name='激活状态', default=True)
    is_binded = models.BooleanField(verbose_name='是否绑定', default=False)

    class Meta:
        verbose_name = "银行卡信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.card_id
