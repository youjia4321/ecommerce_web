from django.shortcuts import render, HttpResponse, reverse, redirect
from card.models import CardInfo
from django.views.generic.base import View
from card.forms import ShowForm, CardRegisterForm, SaveForm, TransferForm
import random
from django.contrib.auth.hashers import make_password, check_password
from users.models import UserProfile
from goods.models import GoodsInfo, GoodsDeal
from users.views import captcha
from datetime import datetime
from users.models import Address
# Create your views here.


# check函数  检查数据库中是否存在词银行卡并且密码相同 存在且密码正确则返回这个银行卡对象 反之返回None
def check(request, card_id, password):
    try:
        card = CardInfo.objects.get(card_id=card_id)
        if make_password(password, 'a', 'pbkdf2_sha256') == card.card_password:
            # if card.user.username == request.user.username:
            return card
    except Exception as e:
        return None

# 进入银行中心首页的视图函数
def getBank(request):
    if request.user.is_authenticated:
        # 如果没有登录用户 则返回到登录界面
        return render(request, 'index_b.html', {})
    return render(request, 'login.html', {'captcha': captcha()})


# 银行卡注册操作
class CardRegisterView(View):
    # randomCardId生成随机的不相同的银行卡号
    def randomCardId(self):
        while True:
            str = ""
            for _ in range(6):
                ch = chr(random.randrange(ord('0'), ord('9') + 1))
                str += ch
            card_id = '611520'+str
            if not CardInfo.objects.filter(card_id=card_id):
                # 如果数据库中不存在此卡号 则生成
                return card_id

    # get方式进入开户界面
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'opencard.html', {})
        return render(request, 'login.html', {'captcha': captcha()})

    # post方式对用户输入的信息进行判断，满足条件则开户成功，反之则在页面显示错误
    def post(self, request):
        cardregister_form = CardRegisterForm(request.POST)
        if cardregister_form.is_valid():
            card_person = UserProfile.objects.get(username=request.user.username)
            cards = card_person.user_card.all()
            card_id = self.randomCardId()
            pass_word = request.POST.get("card_password", "")
            if len(pass_word) != 6:
                return render(request, "opencard.html", {'msg': '输入6位数密码'})
            if not pass_word.isdigit():
                return render(request, "opencard.html", {'msg': '输入6位数字'})
            card_money = request.POST.get("card_money", "")
            try:
                if int(card_money) <= 10 or int(card_money) >= 50000:
                    return render(request, "opencard.html", {'msg': '不能小于10或者大于50000'})
            except:
                return render(request, "opencard.html", {'msg': '输入正确的金额'})
            if len(cards) >= 5:
                return render(request, "opencard.html", {'msg': '你开通的银行卡已达上限'})
            pass_word = make_password(pass_word, 'a', 'pbkdf2_sha256')
            CardInfo.objects.create(user=card_person, card_id=card_id, card_password=pass_word, card_money=card_money)
            return render(request, "opencard.html", {'card_id': card_id})
        else:
            return render(request, "opencard.html", {'cardregister_form': cardregister_form})


# 管理银行卡 查看自己的银行卡并且哪些未绑定可已绑定
class profileCard(View):
    def get(self, request):
        if request.user.is_authenticated:
            cardzip = {}
            user = UserProfile.objects.get(username=request.user.username)
            cards = user.user_card.all().order_by('id')
            for card in cards:
                if card.is_binded  == True:
                    cardzip[card] = '已绑定'
                else:
                    cardzip[card] = '可绑定'
            return render(request, 'profilecard.html' ,{'cards': cards, 'cardzip': cardzip})
        return render(request, 'login.html', {'captcha': captcha()})


# 简单的银行联系页面
def contact(request):
    if request.user.is_authenticated:
        return render(request, 'contact.html', {})
    return render(request, 'login.html', {'captcha': captcha()})


# 查询 用户查询自己的银行卡
class queryCard(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'querycard.html', {})
        return render(request, 'login.html', {'captcha': captcha()})

    def post(self, request):
        show_form = ShowForm(request.POST)
        if show_form.is_valid():
            card_id = request.POST.get('card_id', '')
            card_password = request.POST.get('card_password', '')
            card = check(request, card_id, card_password)
            if card is not None:
                return render(request, 'querycard.html', {'card': card})
            else:
                return render(request, 'querycard.html', {'msg': '银行卡不存在或密码错误'})
        else:
            return render(request, 'querycard.html', {'show_form': show_form})


# 存钱 用户存钱
class saveMoney(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'savecard.html', {})
        return render(request, 'login.html', {'captcha': captcha()})
    
    def post(self, request):
        save_form = SaveForm(request.POST)
        if save_form.is_valid():
            data = save_form.cleaned_data
            card = check(request, data['card_id'], data['card_password'])
            if card is not None:
                if int(data['card_money']) > 0 and int(data['card_money']) <= 100000:
                    card.card_money = card.card_money + int(data['card_money'])
                    card.save()
                    return render(request, 'savecard.html', {'card': card, 'savemoney': data['card_money']})
                else:
                    return render(request, 'savecard.html', {'msg': '输入金额有误', 'save_form': save_form})
            else:
                return render(request, 'savecard.html', {'msg': '银行卡不存在或密码错误', 'save_form': save_form})
        else:
            return render(request, 'savecard.html', {'save_form': save_form})


# 绑定、解除银行卡后台操作
def bindedCard(request, card_id):
    if  request.method == "POST":
        element = "password"+str(card_id)
        password = request.POST.get(element, '')
        card = CardInfo.objects.get(id=card_id)
        if make_password(password, 'a', 'pbkdf2_sha256') == card.card_password:
            if card.is_binded == True:
                card.is_binded = False
            else:
                card.is_binded = True
            card.save()
            return redirect(reverse("profile_card", args=[]))
        else:
            return render(request, 'profilecard.html', {'error_msg': "Wrong password!"})
    return redirect(reverse("profile_card", args=[]))



# 用户的转账操作
class transferCard(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'transfer.html', {})
        return render(request, 'login.html', {'captcha': captcha()})

    def post(self, request):
        transfer_form = TransferForm(request.POST)
        if transfer_form.is_valid():
            data = transfer_form.cleaned_data
            card1 = check(request, data['card_id1'], data['card_password'])
            if card1 is not None:
                try:
                    card2 = CardInfo.objects.filter(card_id = data['card_id2'])[0]
                    if data['card_id1'] == data['card_id2']:
                        return render(request, 'transfer.html', {'msg': '不能向同一张银行卡转账', 'transfer_form': transfer_form})
                    if int(data['card_money']) > 0 and int(data['card_money']) <= 100000:
                        if int(card1.card_money) >= int(data['card_money']):
                            card1.card_money = card1.card_money - int(data['card_money'])
                            card2.card_money = card2.card_money + int(data['card_money'])
                            card1.save()
                            card2.save()
                            return render(request, 'transfer.html', 
                            {'card1': card1, 'transfermoney': data['card_money']})
                        else:
                            return render(request, 'transfer.html', {'msg': '账户余额不足', 'transfer_form': transfer_form})
                    return render(request, 'transfer.html', {'msg': '输入金额有误', 'transfer_form': transfer_form})
                except:
                    return render(request, 'transfer.html', {'transfer_form': transfer_form, 'msg': '对方卡号不存在'})
            else:
                return render(request, 'transfer.html', 
                {'msg': '银行卡不存在或密码错误', 'transfer_form': transfer_form})
        else:
            return render(request, 'transfer.html', {'transfer_form': transfer_form})


# 注销银行卡页面
class cancelCard(View):
    def get(self, request):
        if request.user.is_authenticated:
            user = UserProfile.objects.get(username=request.user.username)
            cards = user.user_card.all().order_by('id')
            return render(request, 'cancel.html', {'cards': cards})
        return render(request, 'login.html', {'captcha': captcha()})


# 注销银行卡操作
def canceledCard(request, card_id):
    if  request.method == "POST":
        element = "password"+str(card_id)
        password = request.POST.get(element, '')
        card = CardInfo.objects.get(id=card_id)
        if make_password(password, 'a', 'pbkdf2_sha256') == card.card_password:
            card.delete()
            return redirect(reverse("cancelCard", args=[]))
        else:
            return render(request, 'cancel.html', {'error_msg': "Wrong password!"})
    return redirect(reverse("cancelCard", args=[]))


# 保存收货人信息
def saveAddress(request):
    if request.is_ajax():
        user = request.user
        address = request.GET.get('address', '')
        mobile = request.GET.get('mobile', '')
        user.mobile = mobile
        user.save()
        address = Address.objects.create(address=address)
        address.user.add(user)
        return HttpResponse('success')


# 支付页面
def bindCard(request):
    if request.user.is_authenticated:
        all_money = request.POST.get('all_money', '')
        all_id = request.POST.get('all_id', '')
        user = UserProfile.objects.get(username=request.user.username)
        cards = user.user_card.all().order_by('id')
        is_bind = []
        not_bind = []
        for card in cards:
            if card.is_binded == True:
                is_bind.append(card)
            else:
                not_bind.append(card)
        return render(request, 'bindcard.html', {'is_bind': is_bind, 'not_bind': not_bind, 'cards': cards, 'all_money': all_money, 'all_id': all_id})
    return render(request, 'login.html', {'captcha': captcha()})


# 商品支付
def payFor(request, card_id):
    if  request.method == "POST":
        all_id = request.POST.get('all_id'+str(card_id), '')
        try:
            ids = all_id.split(",")
        except:
            ids = []
            ids.append(all_id)
        element = "password"+str(card_id)
        money = "pay"+str(card_id)
        password = request.POST.get(element, '')
        pay_money = request.POST.get(money, '')
        card = CardInfo.objects.get(id=card_id)
        user = request.user
        if make_password(password, 'a', 'pbkdf2_sha256') == card.card_password:
            if int(pay_money) >= 0 and card.card_money >= int(pay_money):
                card.card_money = card.card_money - int(pay_money)
                card.save()
                for good in ids:
                    g = GoodsInfo.objects.get(id=good)
                    g.order.add(user)
                    g.goodBus.remove(user)
                    cov = GoodsDeal.objects.create(good_id=g.id, name=g.name, image=g.image, price=g.price, deal_time=datetime.now())
                    cov.success.add(user)

                return render(request, 'bindcard.html', 
                {'error_msg': "Pay for success!", 'card': card, 'money': pay_money})
            else:
                return render(request, 'bindcard.html', 
                {'error_msg': "Lack of balance!", 'card': card, 'money': pay_money})
        else:
            return render(request, 'bindcard.html', {'error_msg': "Wrong password!"})
    return redirect(reverse('bind_card', args=[]))


# 订单结算
def dealCal(request):
    if request.method == 'GET':
        all_id = request.GET.get('all_id', '')
        try:
            ids = all_id.split(',')
        except:
            ids = []
            ids.append(all_id)
        goods = []
        for id in ids:
            good = GoodsInfo.objects.get(id=id)
            goods.append(good)
        all_money = request.GET.get('all_money', '')
        return render(request, 'dingdanjiesuan.html', {'all_money': all_money, 'goods': goods, 'all_id': all_id, 'all_money': all_money})