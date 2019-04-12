from django.contrib import admin
from card.models import CardInfo
# Register your models here.


class CardInfoAdmin(admin.ModelAdmin):
    list_display = ('user', 'card_id', 'card_money')


admin.site.register(CardInfo, CardInfoAdmin)
