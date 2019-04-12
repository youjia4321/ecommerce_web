from django.db import models
from tinymce.models import HTMLField
from datetime import datetime
from users.models import UserProfile
# Create your models here.


class Category(models.Model):
    label = models.CharField(max_length=50, verbose_name='分类标签')

    class Meta:
        verbose_name = '类别'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.label


class GoodsInfo(models.Model):
    name = models.CharField(max_length=150, verbose_name='商品名称')
    introduction = HTMLField(default='暂无简介', verbose_name='商品简介')
    image = models.ImageField(upload_to='goods', default='', max_length=300, verbose_name='商品图片')
    price = models.IntegerField(verbose_name='商品价格')
    visit = models.IntegerField(default=0, verbose_name='浏览量')
    address = models.CharField(max_length=100, null=True, blank=True, verbose_name='商品出产地')
    sell = models.IntegerField(default=0, verbose_name='销售量')
    inventory = models.IntegerField(default=1000, verbose_name='库存')
    category = models.ForeignKey(Category, verbose_name='类别', on_delete=models.CASCADE, null=True, blank=True)
    goodBus = models.ManyToManyField(UserProfile, related_name='user_buys', verbose_name='购物车', blank=True)
    order = models.ManyToManyField(UserProfile, related_name='user_orders', verbose_name='订购', blank=True)
    success = models.ManyToManyField(UserProfile, related_name='user_success', verbose_name='订购成功', blank=True)

    # 先查询到用户的信息 然后查询用户关联的所有购物车商品对象和收藏商品的对象
    # user = UserProfile.objects.get(id=1)
    # goodBus = user.user_buys.all()

    class Meta:
        verbose_name = '商品信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Comment(models.Model):
    good = models.ForeignKey(GoodsInfo, related_name='good_comment', verbose_name='商品', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name='用户')
    email = models.EmailField(max_length=150, verbose_name='邮箱')
    content = models.CharField(max_length=300, verbose_name='内容')
    pub = models.DateTimeField(default=datetime.now, verbose_name='评论时间')

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.good)


class GoodsDeal(models.Model):
    good_id = models.IntegerField(verbose_name='商品编号')
    name = models.CharField(max_length=150, verbose_name='商品名称')
    image = models.ImageField(upload_to='goods', default='', max_length=300, verbose_name='商品图片')
    price = models.IntegerField(verbose_name='商品价格')
    deal_time = models.DateTimeField(default=datetime.now, verbose_name='订单时间')
    flag = models.BooleanField(verbose_name='是否收货', default=False)
    success = models.ManyToManyField(UserProfile, related_name='deal_success', verbose_name='订购成功', blank=True)

    class Meta:
        verbose_name = '商品订单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name