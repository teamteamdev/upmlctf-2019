# UPML CTF 2019 — [bank Bank] CTF

23 февраля 2019 года | [Официальный сайт](https://ctf.upml.tech/2019/) | **[Результаты](SCOREBOARD.md)**

## Таски

Каждая директория содержит один таск с платформы: `README.md` — условие, `WRITEUP.md` — райтап, `task.yaml` — конфиг для борды, остальные файлы — вложения

* [Welcome aboard](tasks/start/) (misc 10)
    * [Ожидание](tasks/wait/) (web 100)
        * [Ограбление 1.0](tasks/grab1/) (telegram 100)
        * [Ограбление 2.0](tasks/grab2/) (telegram 200)
    * [Послание сисадмина](tasks/admin/) (network 100)
        * [DNS-сервера](tasks/dns/) (network 200)
            * [Исходные коды](tasks/code/) (web 100)
                * [Сервер исходных кодов](tasks/codeserver/) (misc 100)
                    * [Hidden backdoor](tasks/backdoor/) (web 250)
            * [Обман системы](tasks/corpflag/) (telegram 400)
    * [Глубина](tasks/inbox/) (recon 200)
        * [CEO](tasks/ceo/) (recon 150)
            * [Проникновение](tasks/naive/) (joy 300)
    * [Правила](tasks/tos/) (misc 150)
        * [Staff only](tasks/insider/) (recon 50)
    * [Скайп](tasks/skype/) (recon 50)
        * [SSL Secrets](tasks/ssl/) (stegano 100)
            * [Where am I?](tasks/newbie/) (network 150)
            * [Сисадмин](tasks/wallpaper/) (network 200)
            * [Парольный менеджер](tasks/mail20/) (recon 100)
                * [The Big Boss](tasks/theboss/) (recon 500)

## Инфраструктура

Вся инфраструктура банка размещена в `infrastructure/`

* [bankbank.exposed](infrastructure/landing/) — лендинг банка
* [ns1.bankbank.exposed](infrastructure/dns/) — конфигурация DNS-сервера
* [botapi.bankbank.exposed](infrastructure/bot/) — Telegram-бот
* [crm.bankbank.tech](infrastructure/crm/) — CRM
* [ftp.bankbank.tech](infrastructure/ftp/) — FTP-сервер
* [vpn.bankbank.tech](infrastructure/vpn/) — VPN-сервер
* [192.168.24.147](infrastructure/dummy/) — веб-сервер во внутрянке
* [192.168.24.226](infrastructure/win/) — Windows XP host
* [connect.yandex.ru](infrastructure/staff/) — Яндекс.Коннект
* [лсд-клуб.рф](insfrastructure/phpbb/) — форум «Литное собрание должников»

## Команда соревнования

* [Никита Сычев](https://github.com/nsychev) — директор соревнования, разработчик тасков и инфраструктуры
* [Ярослав Бурматов](https://github.com/javach) — разработчик тасков
* [Ваня Клименко](https://github.com/vanyaklimenko) — разработчик фронтэнда и тасков
* [Калан Абе](https://github.com/kalan) — разработчик платформы и тасков

## Лицензия

Материалы соревнования можно использовать для тренировок, сборов и других личных целей, но запрещено использовать на своих соревнованиях. Подробнее — [в лицензии](LICENSE)
