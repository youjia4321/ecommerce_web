import xadmin
from card.models import CardInfo


class CardInfoAdmin(object):
    list_display = ['user', 'card_id', 'card_money', 'is_active', 'is_binded', 'open_time']
    search_fields = ['user', 'card_id']
    list_filter = ['user', 'card_id', 'card_money', 'is_active', 'is_binded']


xadmin.site.register(CardInfo, CardInfoAdmin)
