from telegram import *
from telegram.ext import *
from models import *
from enum import Enum
from datetime import datetime
import random, messages, logging, string

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level = logging.INFO)

db.connect()
db.create_tables([Request, Promo, Client, History])

if not Client.get_or_none(Client.card_number == '7313 3700 0000 0004'):
    Client.create(user_id=0, activated=True, name='Service', team_id=-1,
                  state=0, msg_id=0, valid_till='03/19', card_number='7313 3700 0000 0004',
                  cvv='002', balance=100000000, args=[], exploited_1=0, exploited_2=0, exploited_3=0)


class State(Enum):
    WAITING_AUTH_TOKEN = 1
    MAIN_MENU = 2
    ERROR = 3
    TRANSACTION_1 = 4
    TRANSACTION_2 = 5
    TRANSACTION_3 = 6
    TRANSACTION_4 = 7
    SHOP = 8
    SHOP_ERROR = 9
    SHOP_SUCCESS = 10
    PROMO = 11
    PROMO_WRONG = 12
    PROMO_SUCCESS = 13
    ADS = 14


class BankBankBot:
    def __init__(self, token):
        self.updater = Updater(token)
        self.bot = Bot(token)
        self.convs = []
        self.job_queue = self.updater.job_queue

    def start(self):
        self.updater.dispatcher.add_handler(CommandHandler('start', self.start_handler))
        self.updater.dispatcher.add_handler(CommandHandler('flag', self.flag_handler, pass_args=True))
        self.updater.dispatcher.add_handler(MessageHandler(Filters.text, self.message_handler))
        self.updater.dispatcher.add_handler(CallbackQueryHandler(self.callback_query_handler))
        self.updater.dispatcher.add_error_handler(self.error_handler)
        self.updater.start_webhook(listen="10.239.0.4", port=8000)
        self.bot.set_webhook(webhook_url="https://botapi.bankbank.exposed")
        self.updater.idle()

    def start_handler(self, bot, update):
        user_id = update.message.from_user.id
        conv = Conversation.get_conv_by_id(self.convs, user_id)
        if not conv:
            conv = Conversation(user_id, update.message.from_user.username or "Anonym")
            self.convs.append(conv)
        menu = self.generate_menu(conv, None)
        conv.update_menu(bot, menu[0], menu[1])

    def message_handler(self, bot, update):
        user_id = update.message.from_user.id
        text = update.message.text
        conv = Conversation.get_conv_by_id(self.convs, user_id)
        if not conv:
            conv = Conversation(user_id, update.message.from_user.username or "Anonym")
            self.convs.append(conv)
        menu = self.generate_menu(conv, text)
        conv.update_menu(bot, menu[0], menu[1])

    def callback_query_handler(self, bot, update):
        query = update.callback_query
        user_id = query.from_user.id
        conv = Conversation.get_conv_by_id(self.convs, user_id)
        if not conv:
            conv = Conversation(user_id, query.from_user.username.replace('@', '') or "Anonym")
            self.convs.append(conv)
        command = update.callback_query.data.split(':')
        if command[0] == 'to':
            menu = self.generate_menu(conv, command[1], callback=True)
            conv.update_menu(bot, menu[0], menu[1])

    def error_handler(self, bot, update, error):
        logging.error("Update %s caused an error '%s'" % (update, error))

    def generate_menu(self, conv, message, callback=False):
        if conv.state == State.WAITING_AUTH_TOKEN:
            if not message:
                return messages.GREETING, State.WAITING_AUTH_TOKEN
            req = Request.get_or_none(Request.token == message)
            if not req:
                return messages.GREETING_REPEAT, State.WAITING_AUTH_TOKEN
            if req.activated:
                return messages.TOKEN_ALREADY_ACTIVATED, State.WAITING_AUTH_TOKEN
            if req.date > datetime.now():
                return messages.token_wrong_time(req.date), State.WAITING_AUTH_TOKEN
            self.register_client(conv)
            req.activated = True
            req.save()
            return messages.main_menu(conv), State.MAIN_MENU
        if conv.state == State.MAIN_MENU:
            if not callback:
                return messages.main_menu(conv), State.MAIN_MENU
            if message == 'transaction':
                client = conv.get_client()
                if client.balance < 0:
                    return messages.error_money('main_menu'), State.ERROR
                return messages.TRANSACTION_1, State.TRANSACTION_1
            if message == 'shop':
                return messages.SHOP, State.SHOP
            if message == 'promo':
                return messages.PROMO, State.PROMO
            if message == 'ads':
                if conv.get_client().balance <= 0:
                    return messages.ADS_ERROR, State.ADS
                return messages.ads(conv.get_client().card_number.replace(' ', '')), State.ADS
        if conv.state == State.TRANSACTION_1:
            if callback:
                return messages.main_menu(conv), State.MAIN_MENU
            card_number_d = message.replace(' ', '')
            if len(card_number_d) != 16 or not card_number_d.isdigit():
                return messages.TRANSACTION_CARD_DOES_NOT_EXIST, State.TRANSACTION_1
            if self.check_luna([int(x) for x in card_number_d]):
                return messages.TRANSACTION_CARD_DOES_NOT_EXIST, State.TRANSACTION_1
            card_number = ' '.join([card_number_d[i:i+4] for i in range(0, len(card_number_d), 4)])
            other = True
            getter = Client.get_or_none(Client.card_number == card_number)
            if card_number_d[0:6] == '731337':
                other = False
                if not getter:
                    return messages.TRANSACTION_CARD_DOES_NOT_EXIST, State.TRANSACTION_1
                if getter.card_number == conv.get_client().card_number:
                    return messages.TRANSACTION_ERROR_SAME_CARD, State.TRANSACTION_1
            conv.add_arg(card_number)
            return messages.transaction_2(card_number, conv.get_client().balance, other), State.TRANSACTION_2
        if conv.state == State.TRANSACTION_2:
            if callback:
                conv.remove_last_arg()
                return messages.TRANSACTION_1, State.TRANSACTION_1
            if not conv.args:
                return messages.main_menu(conv), State.MAIN_MENU
            client = conv.get_client()
            balance = client.balance
            other = False if conv.args[0][0:7] == '7313 37' else True
            try:
                amount = int(message)
            except:
                return messages.TRANSACTION_INCORRECT_AMOUNT, State.TRANSACTION_2
            if other:
                amount *= 2
            if amount > balance:
                return messages.TRANSACTION_INCORRECT_AMOUNT, State.TRANSACTION_2
            if amount > 100000000 or amount < -1000000000:
                return messages.TRANSACTION_INCORRECT_AMOUNT, State.TRANSACTION_2
            conv.add_arg(amount)
            return messages.transaction_3(conv.args[0], amount, other), State.TRANSACTION_3
        if conv.state == State.TRANSACTION_3:
            if not conv.args:
                return messages.main_menu(conv), State.MAIN_MENU
            comment = message
            client = conv.get_client()
            other = False if conv.args[0][0:7] == '7313 37' else True
            if callback:
                conv.remove_last_arg()
                return messages.transaction_2(conv.args[0], client.balance, other), State.TRANSACTION_2
            conv.transacted = True
            self.job_queue.run_once(self.transaction, 15, context={
                'from_card_number': client.card_number,
                'to_card_number': conv.args[0],
                'amount': conv.args[1],
                'comment': comment,
                'other': other
            })
            res = (messages.transaction_4(conv.args[0], conv.args[1], comment, other), State.TRANSACTION_4)
            conv.remove_args()
            return res
        if conv.state == State.TRANSACTION_4:
            return messages.main_menu(conv), State.MAIN_MENU
        if conv.state == State.ERROR:
            return messages.main_menu(conv), State.MAIN_MENU
        if conv.state == State.SHOP:
            if not callback:
                return messages.SHOP, State.SHOP
            if message == 'main_menu':
                return messages.main_menu(conv), State.MAIN_MENU
            if message == 'buy_flag_1':
                client = conv.get_client()
                if client.balance < 30000:
                    return messages.NOT_ENOUGH_MONEY, State.SHOP_ERROR
                if not client.exploited_1:
                    client.balance = 10000
                    client.save()
                    return messages.error_buy(1), State.SHOP_ERROR
                flag_url = 'https://kor.ill.in.ua/m/610x385/2183718.jpg'
                self.bot.send_photo(conv.user_id, flag_url)
                conv.transacted = True
                self.job_queue.run_once(self.transaction, 0, context={
                    'from_card_number': conv.get_client().card_number,
                    'to_card_number': '7313 3700 0000 0004',
                    'amount': 30000,
                    'comment': 'uctf_o_v1_hacker',
                    'other': False
                })
                return messages.FLAG_MESSAGE, State.SHOP_SUCCESS
            if message == 'buy_flag_2':
                client = conv.get_client()
                if client.balance < 30000:
                    return messages.NOT_ENOUGH_MONEY, State.SHOP_ERROR
                if not client.exploited_2:
                    client.balance = 10000
                    client.save()
                    return messages.error_buy(2), State.SHOP_ERROR
                flag_url = 'https://mtdata.ru/u13/photoA6EF/20910547507-0/original.jpg'
                self.bot.send_photo(conv.user_id, flag_url)
                conv.transacted = True
                self.job_queue.run_once(self.transaction, 0, context={
                    'from_card_number': conv.get_client().card_number,
                    'to_card_number': '7313 3700 0000 0004',
                    'amount': 30000,
                    'comment': 'uctf_v1_ne_podojdal1',
                    'other': False
                })
                return messages.FLAG_MESSAGE, State.SHOP_SUCCESS
            if message == 'buy_flag_3':
                client = conv.get_client()
                if client.balance < 30000:
                    return messages.NOT_ENOUGH_MONEY, State.SHOP_ERROR
                if not client.exploited_3:
                    client.balance = 10000
                    client.save()
                    return messages.error_buy(3), State.SHOP_ERROR
                flag_url = 'https://prousa.info/images/symbols/flag/flag_main/american_flag_waving.jpg'
                conv.transacted = True
                self.bot.send_photo(conv.user_id, flag_url)
                self.job_queue.run_once(self.transaction, 0, context={
                    'from_card_number': conv.get_client().card_number,
                    'to_card_number': '7313 3700 0000 0004',
                    'amount': 30000,
                    'comment': 'uctf_advertisement_abuse',
                    'other': False
                })
                return messages.FLAG_MESSAGE, State.SHOP_SUCCESS
        if conv.state == State.SHOP_ERROR:
            return messages.SHOP, State.SHOP
        if conv.state == State.SHOP_SUCCESS:
            return messages.SHOP, State.SHOP
        if conv.state == State.PROMO:
            if callback:
                return messages.main_menu(conv), State.MAIN_MENU
            promo = Promo.get_or_none(Promo.code == message)
            if not promo:
                return messages.PROMO_WRONG, State.PROMO
            if promo.activated:
                return messages.PROMO_WRONG, State.PROMO
            if conv.get_client().team_id:
                if conv.get_client().team_id != promo.team_id:
                    self.bot.send_message(97631681, 'Player with user_id=%s and team_id=%s tried to activate '
                                                    'promocode %s with team_id=%s' % (conv.user_id,
                                                                                      conv.get_client().team_id,
                                                                                      promo.code,
                                                                                      promo.team_id))
                return messages.PROMO_WRONG, State.PROMO
            promo.activated = True
            promo.save()
            client = conv.get_client()
            client.team_id = promo.team_id
            client.save()
            conv.transacted = True
            self.job_queue.run_once(self.transaction, 1, {
                'from_card_number': '7313 3700 0000 0004',
                'to_card_number': client.card_number,
                'amount': 10000,
                'comment': 'Промокод активирован',
                'other': False
            })
            return messages.PROMO_SUCCESS, State.PROMO_SUCCESS
        if conv.state == State.PROMO_SUCCESS:
            return messages.main_menu(conv), State.MAIN_MENU
        if conv.state == State.ADS:
            return messages.main_menu(conv), State.MAIN_MENU

    def flag_handler(self, bot, update, args):
        if not args:
            bot.send_message(update.message.from_user.id, 'Не указан telegram_id: /flag <telegram_id>')
            return
        user_id = ''.join(args)
        if update.message.from_user.id == 617326093:
            try:
                user_id = int(user_id)
                bot.send_message(user_id, 'Вы получили флаг от администрации банка! uctf_webhookwebhook_exposed')
                client = Client.get_or_none(Client.user_id == user_id)
                if client:
                    client.exploited_3 = True
                    client.save()
                bot.send_message(update.message.from_user.id, 'Флаг отправлен ' + str(user_id))
            except:
                bot.send_message(update.message.from_user.id, 'Данная команда доступна только администрации ПАО '
                                                              '«Финансовая Корпорация «Банк Банк Кредитные Системы»')
        else:
            bot.send_message(update.message.from_user.id, 'Данная команда доступна только администрации ПАО '
                                                          '«Финансовая Корпорация «Банк Банк Кредитные Системы»')

    def transaction(self, bot, job):
        data = job.context
        from_client = Client.get(Client.card_number == data['from_card_number'])
        conv = Conversation.get_conv_by_id(self.convs, from_client.user_id)
        from_team_id = from_client.team_id
        if Client.get_or_none(Client.card_number == data['to_card_number']):
            to_team_id = Client.get(Client.card_number == data['to_card_number']).team_id
            to_user_id = Client.get(Client.card_number == data['to_card_number']).user_id
        else:
            to_team_id = -1
        if from_team_id != -1:
            if not conv.transacted:
                from_client.exploited_2 = True
            conv.transacted = False
        from_short = data['from_card_number'].split(' ')[3]
        to_short = data['to_card_number'].split(' ')[3]
        if to_team_id:
            if from_team_id != to_team_id and to_team_id != -1 and from_team_id != -1:
                self.bot.send_message(97631681, 'Player with user_id=%s and team_id=%s tried to make a '
                                                'transaction to player with user_id=%s '
                                                'and team_id=%s' % (from_client.user_id,
                                                                    from_team_id,
                                                                    to_user_id,
                                                                    to_team_id))
                bot.send_message(from_client.user_id, messages.transaction_another_team(from_short),
                                 parse_mode='HTML')
                return
        from_client.balance -= data['amount']
        from_client.save()
        if from_team_id != -1:
            bot.send_message(from_client.user_id, messages.gave_money(from_short, to_short, data['amount'],
                                                                      from_client.balance,
                                                                      data['comment']), parse_mode='HTML')
        to_client = Client.get_or_none(Client.card_number == data['to_card_number'])
        if to_client:
            to_client.balance += data['amount']
            if to_team_id != -1 and from_team_id != -1:
                to_client.team_id = from_team_id
            to_client.save()
            if to_team_id != -1:
                bot.send_message(to_client.user_id, messages.got_money(from_short, to_short, data['amount'],
                                                                       to_client.balance,
                                                                       data['comment']), parse_mode='HTML')
        if data['amount'] < 0:
            from_client.exploited_1 = True
            from_client.save()
        History.create(from_card=data['from_card_number'], to_card=data['to_card_number'], time=datetime.now(),
                       amount=data['amount'])

    def register_client(self, conv):
        card_number = self.generate_card_number()
        cvv = ''.join([random.choice(string.digits) for _ in range(3)])
        valid_till = '03/19'
        balance = 0
        client = conv.get_client()
        client.activated = True
        client.card_number = card_number
        client.cvv = cvv
        client.valid_till = valid_till
        client.balance = balance
        conv.activated = True
        client.save()

    def generate_card_number(self):
        card_number = '731337' + ''.join([random.choice(string.digits) for _ in range(9)])
        card_number_d = [int(x) for x in card_number]
        for i in range(len(card_number_d)):
            if i % 2 == 0:
                card_number_d[i] *= 2
                if card_number_d[i] > 9:
                    card_number_d[i] -= 9
        last_num = 10 - (sum(card_number_d) % 10)
        card_number = card_number + str(last_num)
        return ' '.join([card_number[i:i+4] for i in range(0, 16, 4)])

    def check_luna(self, number):
        for i in range(len(number) - 1):
            if i % 2 == 0:
                number[i] *= 2
                if number[i] > 9:
                    number[i] -= 9
        if (number[len(number) - 1] + sum(number)) % 10 == 0:
            return True
        return False


class Conversation:
    def __init__(self, user_id, name):
        client = Client.get_or_none(Client.user_id == user_id)
        if client:
            self.user_id = client.user_id
            self.activated = client.activated
            self.name = client.name
            self.state = State(client.state)
            self.msg_id = client.msg_id
            self.args = client.args
            self.transacted = False
        else:
            self.user_id = user_id
            self.activated = False
            self.name = name
            self.state = State.WAITING_AUTH_TOKEN
            self.msg_id = None
            self.args = []
            self.transacted = False
            Client.create(user_id=self.user_id, activated=self.activated, name=self.name,
                          state=self.state.value, msg_id=self.msg_id,
                          exploited_1=False, exploited_2=False, exploited_3=False)

    def update_menu(self, bot, msg, state):
        if self.msg_id:
            try:
                bot.delete_message(self.user_id, self.msg_id)
            except:
                pass
        msg = bot.send_message(self.user_id, msg['text'], reply_markup=msg['markup'], parse_mode='HTML')
        self.msg_id = msg.message_id
        self.state = state
        client = self.get_client()
        client.msg_id = self.msg_id
        client.state = self.state.value
        client.save()

    def get_client(self):
        return Client.get(Client.user_id == self.user_id)

    def add_arg(self, value):
        self.args.append(value)
        client = self.get_client()
        client.args = self.args
        client.save()

    def remove_last_arg(self):
        self.args.pop(len(self.args) - 1)
        client = self.get_client()
        client.args = self.args
        client.save()

    def remove_args(self):
        self.args = []
        client = self.get_client()
        client.args = []
        client.save()

    @staticmethod
    def get_conv_by_id(convs, user_id):
        for conv in convs:
            if user_id == conv.user_id:
                return conv
        return None
