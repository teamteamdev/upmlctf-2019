from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime

GREETING = {
    'text': 'Приветствуем вас в официальном боте [bank Bank] Банка (Банка Банка)!'
            ' Для того, чтобы зарегистрировать личный кабинет, введите токен '
            'авторизации',
    'markup': InlineKeyboardMarkup([])
}

GREETING_REPEAT = {
    'text': 'Токен авторизации неверен. Пожалуйста, введите верный токен авторизации '
            'или зарегистрируйте его на <a href="https://bankbank.exposed">bankbank.exposed</a>.',
    'markup': InlineKeyboardMarkup([])
}

TOKEN_ALREADY_ACTIVATED = {
    'text': 'Данный токен уже активирован. Пожалуйста, введите другой токен или зарегистрируйте новый'
            ' токен на <a href="https://bankbank.exposed">bankbank.exposed</a>',
    'markup': InlineKeyboardMarkup([])
}

TRANSACTION_1 = {
    'text': '<b>Перевод на другую карту</b>\n\n'
            'Введите номер пополняемой карты в формате XXXX XXXX XXXX XXXX.\n\n'
            '<i>Обратите внимание, что если данная карта является картой Банка Банка, '
            'перевод будет осуществлён без комиссии. В противном случае комиссия составит 100%.</i>',
    'markup': InlineKeyboardMarkup([
        [InlineKeyboardButton(text='Назад', callback_data='to:main_menu')]
    ])
}

TRANSACTION_CARD_DOES_NOT_EXIST = {
    'text': '<b>Перевод на другую карту</b>\n\n'
            'Данной карты не существует. Попробуйте ещё раз.',
    'markup': InlineKeyboardMarkup([
        [InlineKeyboardButton(text='Назад', callback_data='to:main_menu')]
    ])
}

TRANSACTION_INCORRECT_AMOUNT = {
    'text': '<b>Перевод на другую карту</b>\n\n'
            'Сумма введена некорректно либо превышает количество денег на счету. Пожалуйста,'
            ' при переводе на карту другого банка учитывайте комиссию в 100%.\n'
            'Попробуйте ещё раз.',
    'markup': InlineKeyboardMarkup([
        [InlineKeyboardButton(text='Назад', callback_data='to:transaction')]
    ])
}

SHOP = {
    'text': 'Приветствуем вас в <b>Официальном Магазине Банка Банка!</b> Здесь '
            'мы продаём товары наших спонсоров по заниженной цене.\n\n'
            '<b>Список товаров:</b>\n\n'
            '<b>1. «‎Флаг украинский»‎</b>\n'
            '<b>Цена:</b> <code>30000</code> RUB\n'
            '<b>Продавец:</b> Служба безопасности Украины\n\n'
            '<b>2. «Флаг советский‎»</b>\n'
            '<b>Цена:</b> <code>30000</code> RUB\n'
            '<b>Продавец:</b> Комитет государственной безопасности СССР\n\n'
            '<b>3. «Флаг навальный»</b>\n'
            '<b>Цена:</b> <code>30000</code> RUB\n'
            '<b>Продавец:</b> Военно-морские силы США',
    'markup': InlineKeyboardMarkup([
        [InlineKeyboardButton(text='Купить товар #1', callback_data='to:buy_flag_1')],
        [InlineKeyboardButton(text='Купить товар #2', callback_data='to:buy_flag_2')],
        [InlineKeyboardButton(text='Купить товар #3', callback_data='to:buy_flag_3')],
        [InlineKeyboardButton(text='Назад', callback_data='to:main_menu')]
    ])
}

FLAG_MESSAGE = {
    'text': 'Товар успешно куплен! Примерное время доставки товара: 5-10 лет. Спасибо вам за использование '
            'платёжной системы Банка Банка!',
    'markup': InlineKeyboardMarkup([
        [InlineKeyboardButton(text='Вернуться в магазин', callback_data='to:shop')]
    ])
}

TRANSACTION_ERROR_SAME_CARD = {
    'text': 'Вы не можете перевести деньги на собственную карту. Пожалуйста, введите другой '
            'номер карты.',
    'markup': InlineKeyboardMarkup([
        [InlineKeyboardButton(text='Назад', callback_data='to:main_menu')]
    ])
}

NOT_ENOUGH_MONEY = {
    'text': 'Недостаточно денег на счёте для покупки данного товара.',
    'markup': InlineKeyboardMarkup([
        [InlineKeyboardButton(text='Назад', callback_data='to:shop')]
    ])
}

PROMO = {
    'text': 'Введите промокод.',
    'markup': InlineKeyboardMarkup([
        [InlineKeyboardButton(text='Назад', callback_data='to:main_menu')]
    ])
}

PROMO_SUCCESS = {
    'text': 'Промокод успешно активирован. На вашу карту зачислено <code>10000</code> RUB.\n\nПодарок дня — флаг: <b>uctf_kaef_mode_on</b>',
    'markup': InlineKeyboardMarkup([
        [InlineKeyboardButton(text='В главное меню', callback_data='to:main_menu')]
    ])
}

PROMO_WRONG = {
    'text': 'Промокод не найден или уже активирован. Проверьте правильность написания или воспользуйтесь '
            'другим промокодом.',
    'markup': InlineKeyboardMarkup([
        [InlineKeyboardButton(text='Назад', callback_data='to:main_menu')]
    ])
}

ADS_ERROR = {
    'text': 'Банк Банк предоставляет своим клиентам возможность постоянного заработка! '
            'Представьте: вам больше не придётся ходить на работу! Всего лишь просматривайте рекламу '
            'и заработывайте за каждый просмотр!\n'
            'К сожалению, пользователи с отрицательным или нулевым балансом не могут воспользоваться'
            ' этой программой.',
    'markup': InlineKeyboardMarkup([
        [InlineKeyboardButton(text='В главное меню', callback_data='to:main_menu')]
    ])
}


def ads(card):
    return {
        'text': 'Банк Банк предоставляет своим клиентам возможность постоянного заработка! '
                'Представьте: вам больше не придётся ходить на работу! Всего лишь просматривайте рекламу '
                'и заработывайте за каждый просмотр!\n'
                'Начните зарабатывать прямо сейчас, '
                '<a href="https://earn.bankbank.tech/?card=%s">перейдите по ссылке</a>' % (card),
        'markup': InlineKeyboardMarkup([
            [InlineKeyboardButton(text='В главное меню', callback_data='to:main_menu')]
        ])
    }


def error_buy(i):
    text = ''
    if i == 1:
        text = 'службой безопасности Украины'
    if i == 2:
        text = 'комитетом государственной безопасности СССР'
    if i == 3:
        text = 'военно-морскими силами США'
    return {
        'text': 'Операция заблокирована %s в связи обнаружением подозрительной активности '
                'на вашем аккаунте. По требованию продавца мы вынуждены обнулить ваш счёт. '
                'Попробуйте купить товар позже или купить товар другого продавца.' % text,
        'markup': InlineKeyboardMarkup([
            [InlineKeyboardButton(text='Назад', callback_data='to:shop')]
        ])
    }


def token_wrong_time(dtime):
    return {
        'text': 'Ваша карта ещё не доставлена на наши сервера. '
                'Повторите попытку через %s секунд.' % int((datetime.now() - dtime).total_seconds()),
        'markup': InlineKeyboardMarkup([])
    }


def main_menu(conv):
    client = conv.get_client()
    d = {
        'name': conv.name,
        'card_number': client.card_number,
        'balance': client.balance,
        'valid_till': client.valid_till,
        'cvv': client.cvv
    }
    return {
        'text': '<b>Здравствуйте, %(name)s! Ваш тариф: Kaefный.</b>\n'
                '<b>Номер вашей карты:</b>\n'
                '<code>%(card_number)s</code>\n'
                '<b>Баланс</b>: <code>%(balance)s</code> RUB.\n'
                '<b>Активна до:</b> <code>%(valid_till)s</code>\n'
                '<b>CVV</b>: <code>%(cvv)s</code>' % d,
        'markup': InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Перевод', callback_data='to:transaction'),
                 InlineKeyboardButton(text='Магазин', callback_data='to:shop')],
                [InlineKeyboardButton(text='Активировать промокод', callback_data='to:promo')],
                [InlineKeyboardButton(text='Заработайте!', callback_data='to:ads')]
        ])
    }


def error_money(prev):
    return {
        'text': '<b>Приносим свои извинения, операция не может быть совершена по причине '
                'недостатка денег на счёте.</b>',
        'markup': InlineKeyboardMarkup([
            [InlineKeyboardButton(text='Назад', callback_data='to:%s' % prev)]
        ])
    }


def transaction_2(number, balance, other):
    perc = '100%' if other else '0%'
    return {
        'text': '<b>Перевод на другую карту</b>\n\n'
                'Карта-получатель: <code>%s</code>\n'
                'Введите сумму перевода. Напоминаем, что сейчас на вашей карте <code>%s</code> RUB и '
                'комиссия составит %s.' % (number, balance, perc),
        'markup': InlineKeyboardMarkup([
            [InlineKeyboardButton(text='Назад', callback_data='to:transaction')]
        ])
    }


def transaction_3(number, amount, other):
    perc = '100%' if other else '0%'
    return {
        'text': '<b>Перевод на другую карту</b>\n\n'
                'Карта-получатель: <code>%s</code>\n'
                'Сумма перевода: <code>%s</code> RUB с учётом комиссии (%s)\n\n'
                'Проверьте введённые данные. '
                'Если данные верны, введите комментарий к переводу, и перевод '
                'будет осуществлён.' % (number, amount, perc),
        'markup': InlineKeyboardMarkup([
            [InlineKeyboardButton(text='Назад', callback_data='to:transaction_amount')]
        ])
    }


def transaction_4(number, amount, comment, other):
    perc = '100%' if other else '0%'
    return {
        'text': '<b>Перевод на другую карту</b>\n\n'
                'Карта-получатель: <code>%s</code>\n'
                'Сумма перевода: <code>%s</code> RUB с учётом комиссии (%s)\n'
                'Комментарий: %s\n\n'
                'Перевод осуществляется... Пожалуйста, подождите...' % (number, amount, perc, comment),
        'markup': InlineKeyboardMarkup([
            [InlineKeyboardButton(text='В личный кабинет', callback_data='to:main)menu')]
        ])
    }


def got_money(from_c, to_c, amount, balance, comment):
    time = datetime.now().strftime('%H:%M')
    return '<code>*%s %s</code>\n' \
           'Зачисление <code>%s</code> RUB\n' \
           'Причина: перевод с карты <code>*%s</code>\n' \
           'Сообщение: %s\n' \
           'Баланс: <code>%s</code> RUB' % (to_c, time, amount, from_c, comment, balance)


def gave_money(from_c, to_c, amount, balance, comment):
    time = datetime.now().strftime('%H:%M')
    return '<code>*%s %s</code>\n' \
           'Списание <code>%s</code> RUB\n' \
           'Причина: перевод на карту <code>*%s</code>\n' \
           'Сообщение: %s\n' \
           'Баланс <code>%s</code> RUB' % (from_c, time, amount, to_c, comment, balance)


def transaction_another_team(from_c):
    time = datetime.now().strftime('%H:%M')
    return '<code>*%s %s</code>\n' \
           'Неуспешная попытка перевода денег. Деньги не были списаны.\n' \
           'Причина: перевод на данную карту недоступен\n' % (from_c, time)
