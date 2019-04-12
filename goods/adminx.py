import xadmin
from goods.models import GoodsInfo, Category, Comment, GoodsDeal
from captcha.models import CaptchaStore


class GoodsInfoAdmin(object):
    list_display = ['name', 'price', 'address', 'inventory', 'category']
    search_fields = ['name', 'inventory', 'address', 'category']
    list_filter = ['name', 'price', 'address', 'inventory', 'category']


class CommentAdmin(object):
    list_display = ['good', 'name', 'content', 'pub']
    search_fields = ['name', 'content']
    list_filter = ['good', 'name', 'content', 'pub']


# class GoodsImgAdmin(object):
#     list_display = ['good', 'image', 'width', 'height']
#     search_fields = ['good']
#     list_filter = ['good']


class CategoryAdmin(object):
    list_display = ['label']
    search_fields = ['label']
    list_filter = ['label']


# class Captcha(CaptchaStore):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#     class Meta:
#         verbose_name = '验证码'
#         verbose_name_plural = verbose_name


class CaptchaStoreAdmin(object):
    list_display = ['challenge', 'hashkey']
    search_fields = ['challenge']
    list_filter = ['challenge', 'hashkey']


class GoodsDealAdmin(object):
    list_display = ['name', 'price']
    search_fields = ['name']
    list_filter = ['name', 'price']


xadmin.site.register(Comment, CommentAdmin)
xadmin.site.register(GoodsInfo, GoodsInfoAdmin)
xadmin.site.register(Category, CategoryAdmin)
xadmin.site.register(GoodsDeal, GoodsDealAdmin)
# xadmin.site.register(GoodsImg, GoodsImgAdmin)
xadmin.site.register(CaptchaStore, CaptchaStoreAdmin)
