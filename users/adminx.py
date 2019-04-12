import xadmin
from xadmin import views
from .models import EmailVerifyRecord, UserProfile, Address


class BaseSetting(object):
    # 主体功能，默认为False
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    # 左侧标题
    site_title = '电子商务后台管理系统'
    # 底部
    site_footer = '电子商务在线网'
    # 缩进
    menu_style = 'accordion'


class UserProfileAdmin(object):
    list_display = ['username', 'birthday', 'gender', 'address', 'mobile']
    search_fields = ['username', 'birthday', 'gender', 'address', 'mobile']
    list_filter = ['username', 'birthday', 'gender', 'address', 'mobile']


class EmailVerifyRecordAdmin(object):
    # 列表展示
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']


class AddressAdmin(object):
    list_display = ['address']
    search_fields = ['address']
    list_filter = ['address']


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)

xadmin.site.unregister(UserProfile)
xadmin.site.register(UserProfile, UserProfileAdmin)
xadmin.site.register(Address, AddressAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)