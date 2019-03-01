# DNS-сервер

Настраивается [djbdns](cr.yp.to/djbdns.html) с [поддержкой](http://cr.yp.to/djbdns/tcp.html) TCP.

Используется следующая конфигурация [зоны](zone) и [AXFR](tcp).

Сервер должен слушать на 10.239.0.1.

Дальше через systemd настраиваются `socat`-сервисы, редиректящие трафик
с TCP и UDP-портов 53 внешнего гейта на 10.239.0.1:53: [tcp](dnstcp.service), [udp](dnsudp.service).
