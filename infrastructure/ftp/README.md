# FTP

Поднимаем [vsftpd](https://security.appspot.com/vsftpd.html) с анонимной авторизацией. [Конфиг](vsftpd.conf)

Берем картинки из сервиса Хакергром с UPML CTF 2018 Alpha и кладем на FTP в диру `nudes/`.

Поднимаем OpenVPN [по инструкции](https://www.digitalocean.com/community/tutorials/openvpn-ubuntu-16-04-ru). В сертификате CA в OU вводим флаг.

Удаляем ключи сервера и кладем на FTP всю директорию `openvpn-ca` в диру `vpn/`.

Добавляем пример клиентского конфига в `example-config.ovpn`.
