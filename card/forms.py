from django import forms

class ShowForm(forms.Form):
    card_id = forms.CharField(label='密码', error_messages={'required': '请填写卡号'})
    card_password = forms.CharField(label='密码', error_messages={'required': '请填写密码'})


class CardRegisterForm(forms.Form):
    card_password = forms.CharField(label='密码', error_messages={'required': '请填写密码'})
    card_money = forms.CharField(label='金额', error_messages={'required': '请填写金额'})


class TransferForm(forms.Form):
    card_id1 = forms.CharField(required=True)
    card_id2 = forms.CharField(required=True)
    card_password = forms.CharField(required=True, max_length=18)
    card_money = forms.CharField(required=True)

class SaveForm(forms.Form):
    card_id = forms.CharField(label='密码', error_messages={'required': '请填写卡号'})
    card_password = forms.CharField(label='密码', error_messages={'required': '请填写密码'})
    card_money = forms.CharField(label='金额', error_messages={'required': '请填写金额'})
