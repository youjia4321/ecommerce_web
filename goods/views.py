from django.shortcuts import render, redirect, reverse, HttpResponse
from django.http import HttpResponseRedirect
from django.views.generic.base import View
from goods.models import Category, GoodsInfo, Comment, GoodsDeal
from django.db.models import Q
from pure_pagination import Paginator
from goods.forms import CommentForm
from users.models import UserProfile, Address
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from datetime import datetime

# Create your views here.
def captcha():
    # 验证码，第一次请求（在users.views中已经讲过）
    hashkey = CaptchaStore.generate_key()
    image_url = captcha_image_url(hashkey)
    captcha = {'hashkey': hashkey, 'image_url': image_url}
    # print(captcha)
    return captcha


# ctx是返回的后台获取的数据
def show_image():
    goods = GoodsInfo.objects.filter(category__label="小米明星单品").order_by('id')
    banner = GoodsInfo.objects.filter(category__label="主页banner")[0]
    peijian = GoodsInfo.objects.filter(category__label="小米配件").order_by('id')
    gif = GoodsInfo.objects.filter(category__label="gif").order_by('id')
    gif_3 = GoodsInfo.objects.filter(category__label="gif_3").order_by('id')
    cate_list = Category.objects.filter(Q(label__icontains='小米') | Q(label__icontains='服装') | Q(label__icontains='零食') | Q(label__icontains='鞋子')).order_by('id')

    fuzhuang = GoodsInfo.objects.filter(category__label="服装").order_by('id')[:5]
    lingshi = GoodsInfo.objects.filter(category__label="零食").order_by('id')
    xiezi = GoodsInfo.objects.filter(category__label="鞋子").order_by('id')[:5]
    shuma = GoodsInfo.objects.filter(category__label="数码产品").order_by('id')[:5]
    jiaju = GoodsInfo.objects.filter(category__label="办公家具").order_by('id')[:5]
    jiadian = GoodsInfo.objects.filter(category__label="家电").order_by('id')[:5]

    label = ['服装', '鞋子', '小米明星单品', '零食', '小米配件', '数码产品', '办公家具', "家电"]
    goodsall = [fuzhuang, xiezi, goods, lingshi, peijian[1:6], shuma, jiaju, jiadian]
    zipped = zip(label, goodsall) 

    ctx = {
        'goods': goods,
        'banner': banner,
        'one': peijian[1: 5], 
        'two': peijian[6: 9],
        'a': peijian[0],
        'b': peijian[5],
        'hongmi': peijian[9],
        'more': peijian[10],
        'gif': gif,
        'gif_3': gif_3,
        'cate_list': cate_list,
        'zipped': zipped
    }
    return ctx


# 进入index.html的接口
def index(request):
    ctx = show_image()
    return render(request, 'index.html', ctx)


# 获取指定商品的详情 渲染到前端
class GetGoodDetails(View):
    def get(self, request, good_id):
        good = GoodsInfo.objects.get(id=good_id)
        good.visit = good.visit + 1
        good.save()
        return render(request, 'xiangqing.html', {'good': good})


# 展示商城的所有商品
class GoodList(View):
    def get(self, request):
        goods = GoodsInfo.objects.all().order_by('-id')
        goods_list, p = page_paginator(request, goods, 10)
        # page_paginator是下面写的一个分页方法， goods是一个列表（所有商品）， 10 表示每页展示10个商品
        return render(request, 'liebiao.html', {'goods_list': goods_list, 'page': p})
        # 然后渲染到前端liebiao.html文件，返回的数据有goods_list， page

    def post(self, request):
        pass


# 评价宝贝
class commentGood(View):
    # get方式进入页面
    def get(self, request, good_id):
        if request.user.is_authenticated:
            good = GoodsInfo.objects.get(id=good_id)
            return render(request, 'pingjiabaobei.html', {'good': good})
        return render(request, 'login.html', {'captcha': captcha()})

    # 用户提交评论
    def post(self, request, good_id):
        good = GoodsInfo.objects.get(id=good_id)
        # 同样的获取商品的唯一主键id
        content = request.POST.get('comment', '')
        username = request.user.username
        email = request.user.email
        # 满足后通过POST方法获取username、email、content
        Comment.objects.create(good=good, name=username, email=email, content=content)
        # 然后在数据库中创建（create）相应的商品评论
        return redirect("comment_details/%s" % good_id, permanent=True)        
        # 然后前端页面刷新之后再将此商品的品论展示出来（实时展示，评论之后就展示）



# 查看商品评论
def CommentOp(request, good_id):
    # 参数good_id表示查看指定的商品id为 good_id
    if request.user.is_authenticated:
        # 同样先判断用户是否登录，下勉就不解释了
        good = GoodsInfo.objects.get(id=good_id)
        # 获取这个商品对象
        comments = good.good_comment.all().order_by('-pub')
        comment_list, p = page_paginator(request, comments, 3)
        # 商品和评论在数据表中的关系是一对多，获取这个商品的所有评论并返回给前端
        return render(request, 'comment.html', {'comment_list': comment_list, 'comments': comments})
    return render(request, 'login.html', {'captcha': captcha()})



# 获取用户的购物车详情页面的操作及数据
def get_gouwuche_details(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            username = request.user.username
            user = UserProfile.objects.get(username=username)
            goods = user.user_buys.all()
            number = len(goods)
            sum = 0
            goods_list, p = page_paginator(request, goods, 5)
            return render(request, 'gouwuche.html', {'goods_list': goods_list, 'number': number, 'sum': sum})
        else:
            return render(request, 'login.html', {'captcha': captcha()})
    else:
        pass


# 获取订单中心详情页面的操作及数据
def get_dingdan_details(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            username = request.user.username
            user = UserProfile.objects.get(username=username)
            goods = user.deal_success.all().order_by('-id')
            for good in goods:
                if (datetime.now() - good.deal_time).seconds >= 240: # 时间超过2分钟就变为收货状态
                    good.flag = True
                    good.save()
            goods_list, p = page_paginator(request, goods, 3)
            return render(request, 'dingdanzhongxin.html', {'goods_list': goods_list, 'goods': goods})
        return render(request, 'login.html', {'captcha': captcha()})

# 搜索功能
def search(request):
    key = request.GET.get('key', '')
    goods = GoodsInfo.objects.filter(Q(name__icontains=key) | Q(introduction__icontains=key) | Q(category__label__icontains=key)).order_by('id')
    #  能通过商品的名称、简介、分类字段搜索商品
    goods_list, p = page_paginator(request, goods, 10)
    return render(request, 'results.html', {'goods_list': goods_list, 'goods': goods, 'page': p})


# 分页函数
def page_paginator(request, good, count):
    try:
        page = request.GET.get('page', 1)
    except:
        page = 1
    p = Paginator(good, count, request=request)
    goods_list = p.page(page)
    return goods_list, p


# 添加到购物车
def add_bus(request):
    good_id = request.GET.get('good_id', '')
    good = GoodsInfo.objects.get(id=good_id)
    user = UserProfile.objects.get(username=request.user.username)
    good.goodBus.add(user)
    return redirect(reverse('shopping_bus', args=[]))


# 前端ajax删除购物车中的商品的处理接口
def del_good(request):
    if request.is_ajax():
        del_id = request.GET.get('del_id', '')
        good = GoodsInfo.objects.get(id=del_id)
        user = UserProfile.objects.get(username=request.user.username)
        good.goodBus.remove(user)
    return HttpResponse("success")


# 获取用户的收货地址页面及数据
def address(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            user = UserProfile.objects.get(username=request.user.username)
            address = user.user_address.all().order_by('-id')[:8]
            return render(request, 'address.html', {'address': address})
        return render(request, 'login.html', {'captcha': captcha()})