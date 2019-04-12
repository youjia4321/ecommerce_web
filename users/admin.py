from django.contrib import admin
from users.models import UserProfile, EmailVerifyRecord, Address
# Register your models here.


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("username", "gender", "email", 'mobile', 'money')


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(EmailVerifyRecord)
admin.site.register(Address)