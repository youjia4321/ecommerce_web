from django.contrib import admin
from goods.models import GoodsInfo, Category, Comment, GoodsDeal


class GoodsInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'sell', 'category', 'inventory', 'price', 'address')


# class GoodsImgAdmin(admin.ModelAdmin):
#     list_display = ('good', 'image')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('good', 'name', 'content', 'pub')


admin.site.register(GoodsInfo, GoodsInfoAdmin)
admin.site.register(Category)
admin.site.register(GoodsDeal)
admin.site.register(Comment, CommentAdmin)
# admin.site.register(GoodsImg, GoodsImgAdmin)
