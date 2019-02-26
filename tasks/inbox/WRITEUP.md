# Глубина: Write-up

Заходим в предложенный инстаграм, видим фоточки некоторого Роберта.

Отмечаем два важных факта:

* есть фотография монитора с открытым сайтом ICANN и страницей про смену контактов домена
* есть стикер на мониторе с паролем от «рабочей почты»

Осталось найти почту — для этого давайте сходим и узнаем эти самые контакты домена. Но нас ожидает облом:

```
$ whois bankbank.exposed
Registry Domain ID: 66d50d9639ad4d3db6d3237e81fed069-DONUTS
Registrar WHOIS Server: www.namesilo.com/whois.php
Registrar URL: http://www.namesilo.com
<...>
Registrant Name: REDACTED FOR PRIVACY
Registrant Organization: Bank Bank Credit Systems PJSC
Registrant Street: REDACTED FOR PRIVACY
Registrant City: REDACTED FOR PRIVACY
Registrant State/Province: Chelyabinsk district
Registrant Postal Code: REDACTED FOR PRIVACY
Registrant Country: RU
Registrant Phone: REDACTED FOR PRIVACY
Registrant Phone Ext: REDACTED FOR PRIVACY
Registrant Fax: REDACTED FOR PRIVACY
Registrant Fax Ext: REDACTED FOR PRIVACY
Registrant Email: Please query the RDDS service of the Registrar of Record identified in this output for information on how to contact the Registrant, Admin, or Tech contact of the queried domain name.
```

Однако, не сдаемся, и идем в [RDDS-сервис](http://www.namesilo.com/whois.php) регистратора, как нас и просят. И здесь, что удивительно, нам дают полную информацию:

```
Registrant Name: Robert R. Kulikov
Registrant Organization: Bank Bank Credit Systems PJSC
Registrant Street: Office 1, Ejfeleva Tower, 56 Sovetskaya st.
Registrant City: Paris village
Registrant State/Province: Chelyabinsk district
Registrant Postal Code: 457654
Registrant Country: RU
Registrant Phone: +7.8121337322
Registrant Phone Ext: 
Registrant Fax: 
Registrant Fax Ext: 
Registrant Email: kulikov@bankbank.exposed
```

Конечно, по номеру мы звонить не будем — наверняка он фейковый. Но зато у нас есть почта. Также этого человека зовут Роберт, что подтверждает всю картину.

Осталось узнать, где хостится почта Банка, сделаем это одной bash-командой:

```bash
$ dig IN MX bankbank.exposed.
bankbank.exposed.       300     IN      MX      10 mx.yandex.net.
```

Итак, Яндекс.Почта. Идем на [страницу входа](https://mail.yandex.ru/), вводим логин (kulikov@bankbank.exposed), пароль с фотографии (`Za78pix_KEk`) и входим. В почте лежит флаг.

Флаг: **uctf_instanda**
