"""EcommerceWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import xadmin
from django.contrib import admin
from django.urls import path, include
from .settings import MEDIA_ROOT, STATIC_ROOT
from django.conf.urls import url
from django.views.static import serve
from users.views import refresh_captcha, RegisterView, LoginView, Logout, ActiveView
from goods.views import index, GetGoodDetails, search, GoodList, CommentOp, get_gouwuche_details, add_bus, del_good, get_dingdan_details, address, commentGood
from users.views import LoginView, RegisterView, Logout, self_info, page_not_found, changeInfo
from card.views import getBank, CardRegisterView, profileCard, contact, queryCard, saveMoney, bindCard, bindedCard,  transferCard, cancelCard, canceledCard, payFor, dealCal, saveAddress

'''
下面为网页展示的各个接口，例如path('xadmin/', xadmin.site.urls),  在浏览器输入localhost/xadmin就能进入相应的html界面
'''
urlpatterns = [
    path('xadmin/', xadmin.site.urls),  # xadmin后台管理界面
    path('admin/', admin.site.urls), # django自带的后台管理界面
    url(r'^tinymce/', include('tinymce.urls')), # 富文本编辑器的实现，就是在后台插入数据时，管理员能以word的形式写入数据
    url(r'^media/(?P<path>.*)/$', serve, {"document_root": MEDIA_ROOT}),  # 处理上传文件的路径，如商品图片
    url(r'^static/(?P<path>.*)/$', serve, {"document_root": STATIC_ROOT}),  # 渲染静态文件的路径，在前端渲染css、js等
    path('captcha/', include("captcha.urls")),  # 处理验证码路径
    path('refresh_captcha/', refresh_captcha),  # 刷新验证码
    url(r'^active/(?P<active_code>.*)/$', ActiveView.as_view(), name='active_user'), # 用户验证
    path('self_info', self_info, name='self_info'), # 进入个人中心
    path('saveaddress', saveAddress, name='saveaddress'), # 保存用户地址信息
    path('changeinfo', changeInfo, name='changeinfo'), # 修改个人信息

    # 处理路径
    path('', index, name="index"), # 主界面 localhost
    path('login', LoginView.as_view(), name="login"), # 登录界面 
    path('register', RegisterView.as_view(), name="register"), # 注册界面
    path('logout', Logout, name="logout"), # 用户注销
    url(r'^detail/(\d+)/$', GetGoodDetails.as_view(), name='get_good_detail'), # 商品详情页面
    url(r'^serach/$', search, name='search'), # 搜索功能
    path('goods_list', GoodList.as_view(), name='goods_list'), # 所有商品列表
    url(r'comment_details/(\d+)/$', CommentOp, name='get_good_comment'),  # 获取商品评论
    path('shopping_bus', get_gouwuche_details, name='shopping_bus'), # 购物车详情
    path('add_bus', add_bus, name='add_bus'), # 添加购车车操作
    path('del_good', del_good, name='del_good'), # 删除购物车商品
    path('dingdanzhongxin', get_dingdan_details, name='dingdanzhongxin'), # 订单中心
    path('address', address, name='address'), # 用户地址
    url(r'comment_good/(\d+)/$', commentGood.as_view(), name='commentGoods'), # 宝贝评价
    path('dealCal', dealCal, name='dealCal'), # 选购->订单结算

    # bank
    path('bankIndex', getBank, name="bank_index"), # 银行首页
    path('registerCard', CardRegisterView.as_view(), name='register_card'), # 银行卡开户
    path('profileCard', profileCard.as_view(), name='profile_card'), # 管理绑定银行卡
    path('contact', contact, name='contact'), # 联系我们界面
    path('queryCard', queryCard.as_view(), name='query_card'), # 查询操作页面
    path('saveMoney', saveMoney.as_view(), name='save_money'), # 存钱操作页面
    path('bindCard', bindCard, name='bind_card'), # 支付页面
    url(r'bindedCard/(\d+)/$', bindedCard, name='bindedCard'), # 用户绑定和取消绑定操作
    url(r'canceledCard/(\d+)/$', canceledCard, name='canceledCard'), # 用户注销操作
    url(r'payForCard/(\d+)/$', payFor, name='payForCard'), # 支付操作
    path('transferCard', transferCard.as_view(), name='transferCard'), # 转账操作页面
    path('cancelCard', cancelCard.as_view(), name='cancelCard'), # 注销操作页面

]
