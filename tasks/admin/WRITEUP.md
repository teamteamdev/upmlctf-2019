# Послание сисадмина: Write-up

Где мог бы положить флаг __сисадмин__? Возможно, в DNS-записях. Смотрим:

```
$ dig IN TXT bankbank.exposed.

;; ANSWER SECTION:
bankbank.exposed.       299     IN      TXT     "v=spf1 redirect=_spf.yandex.net ~all"
bankbank.exposed.       299     IN      TXT     "uctf_digg3r_3xp3rt_or_n0t"
bankbank.exposed.       299     IN      TXT     "yandex-verification: 70ddd42d9c7067ef"
```

Флаг: **uctf_digg3r_3xp3rt_or_n0t**
